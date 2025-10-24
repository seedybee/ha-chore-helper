"""Constants for the Chore Helper integration."""

from logging import Logger, getLogger

from homeassistant.helpers import selector

LOGGER: Logger = getLogger(__package__)

DOMAIN = "chore_helper"
CALENDAR_NAME = "Chores"
SENSOR_PLATFORM = "sensor"
CALENDAR_PLATFORM = "calendar"
ATTRIBUTION = "Data is provided by chore_helper"
CONFIG_VERSION = 6

ATTR_NEXT_DATE = "next_due_date"
ATTR_DAYS = "days"
ATTR_LAST_COMPLETED = "last_completed"
ATTR_LAST_UPDATED = "last_updated"
ATTR_OVERDUE = "overdue"
ATTR_OVERDUE_DAYS = "overdue_days"
ATTR_OFFSET_DATES = "offset_dates"
ATTR_ADD_DATES = "add_dates"
ATTR_REMOVE_DATES = "remove_dates"
ATTR_ASSIGNED_TO = "assigned_to"
ATTR_ASSIGNED_TO_NAME = "assigned_to_name"
ATTR_ALLOCATION_MODE = "allocation_mode"
ATTR_PEOPLE = "people"

BINARY_SENSOR_DEVICE_CLASS = "connectivity"
DEVICE_CLASS = "chore_helper__schedule"

CONF_SENSOR = "sensor"
CONF_ENABLED = "enabled"
CONF_FORECAST_DATES = "forecast_dates"
CONF_SHOW_OVERDUE_TODAY = "show_overdue_today"
CONF_FREQUENCY = "frequency"
CONF_MANUAL = "manual_update"
CONF_ICON_NORMAL = "icon_normal"
CONF_ICON_TODAY = "icon_today"
CONF_ICON_TOMORROW = "icon_tomorrow"
CONF_ICON_OVERDUE = "icon_overdue"
CONF_OFFSET = "offset"
CONF_DAY_OF_MONTH = "day_of_month"
CONF_DUE_DATE_OFFSET = "due_date_offset"
CONF_FIRST_MONTH = "first_month"
CONF_LAST_MONTH = "last_month"
CONF_CHORE_DAY = "chore_day"
CONF_WEEKDAY_ORDER_NUMBER = "weekday_order_number"
CONF_FORCE_WEEK_NUMBERS = "force_week_order_numbers"
CONF_DATE = "date"
CONF_TIME = "time"
CONF_PERIOD = "period"
CONF_FIRST_WEEK = "first_week"
CONF_START_DATE = "start_date"
CONF_SENSORS = "sensors"
CONF_DATE_FORMAT = "date_format"
CONF_ALLOCATION_MODE = "allocation_mode"
CONF_PEOPLE = "people"
CONF_MULTIPLE_PEOPLE_MODE = "multiple_people_mode"
CONF_RECURRENCE_TYPE = "recurrence_type"
CONF_DAILY_PATTERN = "daily_pattern"
CONF_WEEKLY_PATTERN = "weekly_pattern"
CONF_MONTHLY_PATTERN = "monthly_pattern"
CONF_YEARLY_PATTERN = "yearly_pattern"
CONF_WEEKLY_DAYS = "weekly_days"
CONF_DAY_TYPE = "day_type"
CONF_END_TYPE = "end_type"
CONF_END_DATE = "end_date"
CONF_END_AFTER_OCCURRENCES = "end_after_occurrences"

DEFAULT_NAME = DOMAIN
DEFAULT_FIRST_MONTH = "jan"
DEFAULT_LAST_MONTH = "dec"
DEFAULT_FREQUENCY = "every-n-days"
DEFAULT_PERIOD = 1
DEFAULT_FIRST_WEEK = 1
DEFAULT_DATE_FORMAT = "%b-%d-%Y"
DEFAULT_FORECAST_DATES = 10
DEFAULT_SHOW_OVERDUE_TODAY = False

DEFAULT_ICON_NORMAL = "mdi:broom"
DEFAULT_ICON_TODAY = "mdi:bell"
DEFAULT_ICON_TOMORROW = "mdi:bell-outline"
DEFAULT_ICON_OVERDUE = "mdi:bell-alert"
ICON = DEFAULT_ICON_NORMAL

STATE_TODAY = "today"
STATE_TOMORROW = "tomorrow"

FREQUENCY_OPTIONS = [
    selector.SelectOptionDict(value="every-n-days", label="Every [x] days"),
    selector.SelectOptionDict(value="every-n-weeks", label="Every [x] weeks"),
    selector.SelectOptionDict(value="every-n-months", label="Every [x] months"),
    selector.SelectOptionDict(value="every-n-years", label="Every [x] years"),
    selector.SelectOptionDict(value="after-n-days", label="After [x] days"),
    selector.SelectOptionDict(value="after-n-weeks", label="After [x] weeks"),
    selector.SelectOptionDict(value="after-n-months", label="After [x] months"),
    selector.SelectOptionDict(value="after-n-years", label="After [x] years"),
    selector.SelectOptionDict(value="blank", label="Manual"),
]

DAILY_FREQUENCY = ["every-n-days", "after-n-days"]
WEEKLY_FREQUENCY = ["every-n-weeks", "after-n-weeks"]
MONTHLY_FREQUENCY = ["every-n-months", "after-n-months"]
YEARLY_FREQUENCY = ["every-n-years", "after-n-years"]
BLANK_FREQUENCY = ["blank"]

WEEKDAY_OPTIONS = [
    selector.SelectOptionDict(value="0", label="None"),
    selector.SelectOptionDict(value="mon", label="Monday"),
    selector.SelectOptionDict(value="tue", label="Tuesday"),
    selector.SelectOptionDict(value="wed", label="Wednesday"),
    selector.SelectOptionDict(value="thu", label="Thursday"),
    selector.SelectOptionDict(value="fri", label="Friday"),
    selector.SelectOptionDict(value="sat", label="Saturday"),
    selector.SelectOptionDict(value="sun", label="Sunday"),
]

MONTH_OPTIONS = [
    selector.SelectOptionDict(value="jan", label="January"),
    selector.SelectOptionDict(value="feb", label="February"),
    selector.SelectOptionDict(value="mar", label="March"),
    selector.SelectOptionDict(value="apr", label="April"),
    selector.SelectOptionDict(value="may", label="May"),
    selector.SelectOptionDict(value="jun", label="June"),
    selector.SelectOptionDict(value="jul", label="July"),
    selector.SelectOptionDict(value="aug", label="August"),
    selector.SelectOptionDict(value="sep", label="September"),
    selector.SelectOptionDict(value="oct", label="October"),
    selector.SelectOptionDict(value="nov", label="November"),
    selector.SelectOptionDict(value="dec", label="December"),
]

ORDER_OPTIONS = [
    selector.SelectOptionDict(value="0", label="None"),
    selector.SelectOptionDict(value="1", label="1st"),
    selector.SelectOptionDict(value="2", label="2nd"),
    selector.SelectOptionDict(value="3", label="3rd"),
    selector.SelectOptionDict(value="4", label="4th"),
    selector.SelectOptionDict(value="5", label="5th"),
    selector.SelectOptionDict(value="-1", label="last"),
    selector.SelectOptionDict(value="-2", label="2nd from last"),
    selector.SelectOptionDict(value="-3", label="3rd from last"),
    selector.SelectOptionDict(value="-4", label="4th from last"),
]

ALLOCATION_MODE_OPTIONS = [
    selector.SelectOptionDict(value="none", label="None (No person allocation)"),
    selector.SelectOptionDict(value="single", label="Single person"),
    selector.SelectOptionDict(value="alternating", label="Alternating (rotate on completion)"),
    selector.SelectOptionDict(value="shared", label="Shared (all people)"),
]

MULTIPLE_PEOPLE_MODE_OPTIONS = [
    selector.SelectOptionDict(value="alternating", label="Alternating (rotate on completion)"),
    selector.SelectOptionDict(value="shared", label="Shared (appears for all selected people)"),
]

# Recurrence type options
RECURRENCE_TYPE_OPTIONS = [
    selector.SelectOptionDict(value="daily", label="Daily"),
    selector.SelectOptionDict(value="weekly", label="Weekly"),
    selector.SelectOptionDict(value="monthly", label="Monthly"),
    selector.SelectOptionDict(value="yearly", label="Yearly"),
]

# Daily pattern options
DAILY_PATTERN_OPTIONS = [
    selector.SelectOptionDict(value="every_n_days", label="Every X day(s)"),
    selector.SelectOptionDict(value="every_weekday", label="Every weekday"),
    selector.SelectOptionDict(value="regenerate_days", label="Regenerate every X day(s) after completion"),
]

# Weekly pattern options
WEEKLY_PATTERN_OPTIONS = [
    selector.SelectOptionDict(value="recur_weekly", label="Recur every X week(s) on selected days"),
    selector.SelectOptionDict(value="regenerate_weeks", label="Regenerate every X week(s) after completion"),
]

# Monthly pattern options
MONTHLY_PATTERN_OPTIONS = [
    selector.SelectOptionDict(value="day_of_month", label="Day X of every X month(s)"),
    selector.SelectOptionDict(value="nth_day_type", label="The Xth [day type] of every X month(s)"),
    selector.SelectOptionDict(value="regenerate_months", label="Regenerate every X month(s) after completion"),
]

# Yearly pattern options
YEARLY_PATTERN_OPTIONS = [
    selector.SelectOptionDict(value="month_day", label="Every [month] [day]"),
    selector.SelectOptionDict(value="nth_day_type_of_month", label="The Xth [day type] of [month]"),
    selector.SelectOptionDict(value="regenerate_years", label="Regenerate every X year(s) after completion"),
]

# Day type options (for monthly/yearly nth patterns)
DAY_TYPE_OPTIONS = [
    selector.SelectOptionDict(value="day", label="Day"),
    selector.SelectOptionDict(value="weekday", label="Weekday"),
    selector.SelectOptionDict(value="weekend_day", label="Weekend day"),
    selector.SelectOptionDict(value="monday", label="Monday"),
    selector.SelectOptionDict(value="tuesday", label="Tuesday"),
    selector.SelectOptionDict(value="wednesday", label="Wednesday"),
    selector.SelectOptionDict(value="thursday", label="Thursday"),
    selector.SelectOptionDict(value="friday", label="Friday"),
    selector.SelectOptionDict(value="saturday", label="Saturday"),
    selector.SelectOptionDict(value="sunday", label="Sunday"),
]

# End type options (for range of recurrence)
END_TYPE_OPTIONS = [
    selector.SelectOptionDict(value="no_end", label="No end date"),
    selector.SelectOptionDict(value="end_by_date", label="End by"),
    selector.SelectOptionDict(value="end_after_occurrences", label="End after X occurrences"),
]

DEFAULT_ALLOCATION_MODE = "none"
DEFAULT_RECURRENCE_TYPE = "daily"
DEFAULT_END_TYPE = "no_end"
