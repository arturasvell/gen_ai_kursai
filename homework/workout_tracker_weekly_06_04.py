from utils.input_utils import expect_for_valid_integer_input

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

minutes_per_day:list[float] = []
for weekday in weekdays:
    print(f"Write minutes exercised on {weekday}:")
    workout_length = expect_for_valid_integer_input(0)
    minutes_per_day.append(workout_length)

weekly_goal = 170
total_time = sum(minutes_per_day)
print(f"Total time this week: {total_time}")
print(f"Day with the longest workout: {weekdays[minutes_per_day.index(max(minutes_per_day))]}")
print(f"Was the weekly goal met? {total_time >= weekly_goal}")