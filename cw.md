To create AWS CloudWatch cron expressions for running a job Monday to Friday at 9:00 AM EST and 12:30 PM EST, you need to consider the format and time zone support in AWS. AWS CloudWatch cron expressions follow the format: `cron(Minutes Hours Day-of-month Month Day-of-week Year)`.

For EST (Eastern Standard Time), you must consider that AWS cron expressions are in UTC. EST is UTC-5 during standard time and UTC-4 during daylight saving time (EDT).

### For 9:00 AM EST:
- During Standard Time (UTC-5): 9:00 AM EST is 14:00 UTC.
- During Daylight Saving Time (UTC-4): 9:00 AM EDT is 13:00 UTC.

### For 12:30 PM EST:
- During Standard Time (UTC-5): 12:30 PM EST is 17:30 UTC.
- During Daylight Saving Time (UTC-4): 12:30 PM EDT is 16:30 UTC.

AWS does not automatically adjust for daylight saving time, so you need to account for it manually or set up multiple rules. 

### Cron Expressions:
1. **9:00 AM EST (14:00 UTC during standard time, 13:00 UTC during daylight saving time):**
   - Standard Time: `cron(0 14 ? * MON-FRI *)`
   - Daylight Saving Time: `cron(0 13 ? * MON-FRI *)`

2. **12:30 PM EST (17:30 UTC during standard time, 16:30 UTC during daylight saving time):**
   - Standard Time: `cron(30 17 ? * MON-FRI *)`
   - Daylight Saving Time: `cron(30 16 ? * MON-FRI *)`

You need to set up these expressions according to the current period (standard or daylight saving time).

### Handling Both Time Changes:
If you want to handle both time changes automatically, you can set two sets of rules:
- One for the period of standard time (typically from the first Sunday in November to the second Sunday in March).
- One for the period of daylight saving time (typically from the second Sunday in March to the first Sunday in November).

### Example for 2024:
- **Standard Time (November 5, 2023, to March 10, 2024):**
  - 9:00 AM EST: `cron(0 14 ? * MON-FRI *)`
  - 12:30 PM EST: `cron(30 17 ? * MON-FRI *)`

- **Daylight Saving Time (March 10, 2024, to November 3, 2024):**
  - 9:00 AM EDT: `cron(0 13 ? * MON-FRI *)`
  - 12:30 PM EDT: `cron(30 16 ? * MON-FRI *)`

Make sure to adjust the cron expressions for the corresponding periods as needed.