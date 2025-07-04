from datetime import datetime, timedelta

class Employee:
    def __init__(self, name, hourly_rate, available_start, available_end):
        self.name = name
        self.hourly_rate = hourly_rate
        self.available_start = available_start
        self.available_end = available_end

class TimeSlot:
    def __init__(self, start_time, end_time, needed_workers):
        self.start_time = start_time
        self.end_time = end_time
        self.needed_workers = needed_workers
        self.business_level = 0.0

class Shift:
    def __init__(self, worker, time_slot):
        self.worker = worker
        self.time_slot = time_slot
class CafeScheduler:
    def __init__(self, business_data):
        self.business_data = business_data
        self.min_shift_hours = 2
        
    def schedule_shifts(self, start_time, end_time, staff_list):
        duration = end_time - start_time
        
        if duration.total_seconds() / 3600 <= self.min_shift_hours:
            return self.assign_staff_to_slot(start_time, end_time, staff_list)
        
        midpoint = start_time + duration / 2
        
        left_busy = self.calculate_business_level(start_time, midpoint)
        right_busy = self.calculate_business_level(midpoint, end_time)
        
        if left_busy > right_busy:
            busy_start, busy_end = start_time, midpoint
            quiet_start, quiet_end = midpoint, end_time
        else:
            busy_start, busy_end = midpoint, end_time
            quiet_start, quiet_end = start_time, midpoint
        
        expensive_staff, cheap_staff = self.split_staff_by_cost(staff_list)
        
        busy_shifts = self.schedule_shifts(busy_start, busy_end, expensive_staff)
        quiet_shifts = self.schedule_shifts(quiet_start, quiet_end, cheap_staff)
        
        return busy_shifts + quiet_shifts
    def calculate_business_level(self, start_time, end_time):
        total = 0.0
        hours = 0
        
        current = start_time
        while current < end_time:
            hour_key = current.weekday() * 24 + current.hour
            total += self.business_data.get(hour_key, 0.5)
            hours += 1
            current += timedelta(hours=1)
        
        return total / hours if hours > 0 else 0.5
    
    def split_staff_by_cost(self, staff_list):
        sorted_staff = sorted(staff_list, key=lambda x: x.hourly_rate)
        middle = len(sorted_staff) // 2
        
        expensive_staff = sorted_staff[middle:]
        cheap_staff = sorted_staff[:middle]
        
        return expensive_staff, cheap_staff
    
    def assign_staff_to_slot(self, start_time, end_time, staff_list):
        business_level = self.calculate_business_level(start_time, end_time)
        
        needed_workers = max(1, int(business_level * 3))
        
        available_staff = []
        for worker in staff_list:
            if (worker.available_start <= start_time and 
                worker.available_end >= end_time):
                available_staff.append(worker)
        
        available_staff.sort(key=lambda x: x.hourly_rate)
        selected_staff = available_staff[:needed_workers]
        
        shifts = []
        for worker in selected_staff:
            slot = TimeSlot(start_time, end_time, needed_workers)
            slot.business_level = business_level
            shifts.append(Shift(worker, slot))
        
        return shifts

def setup_test_data():
    business_data = {}
    
    for hour in range(168):
        day = hour // 24
        time_of_day = hour % 24
        
        if time_of_day in [7, 8, 9, 11, 12, 13, 17, 18, 19]:
            business_data[hour] = 0.8
        elif time_of_day in [10, 14, 15, 16, 20]:
            business_data[hour] = 0.6
        elif time_of_day in [6, 21, 22]:
            business_data[hour] = 0.4
        else:
            business_data[hour] = 0.2
    
    staff = [
        Employee("Alice", 15.0, datetime(2024, 1, 1, 6), datetime(2024, 1, 1, 22)),
        Employee("Bob", 12.0, datetime(2024, 1, 1, 8), datetime(2024, 1, 1, 20)),
        Employee("Charlie", 18.0, datetime(2024, 1, 1, 10), datetime(2024, 1, 1, 18)),
        Employee("Lam", 14.0, datetime(2024, 1, 1, 5), datetime(2024, 1, 1, 23)),
    ]
    
    return business_data, staff

def main():
    business_data, staff = setup_test_data()
    scheduler = CafeScheduler(business_data)
    
    start = datetime(2024, 1, 1, 6)
    end = datetime(2024, 1, 1, 22)
    
    shifts = scheduler.schedule_shifts(start, end, staff)
    
    print("Cafe Schedule:")
    for shift in shifts:
        print(f"{shift.worker.name}: {shift.time_slot.start_time.strftime('%H:%M')} - {shift.time_slot.end_time.strftime('%H:%M')}")

if __name__ == "__main__":
    main()