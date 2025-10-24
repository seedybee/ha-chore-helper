# Chore Helper for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

Forked from VolantisDev/ha-chore-helper to include a person selector for specific chores.
This component allows you to set up and manage all of your recurring household chores
in a flexible way using Home Assistant helpers.

Chore Helper is in its infancy and might not work well for your use case yet. Let me
know how it could be improved!

**This component will set up the following platforms.**

| Platform   | Description                           |
| ---------- | ------------------------------------- |
| `sensor`   | Contains the state for a single chore |
| `calendar` | A Chore calendar for easy tracking    |

This helper is very loosely inspired by the way that the Tody app for Android works,
except it is entirely managed within Home Assistant and benefits from the power of
calendars, automations, and sensors.

## Installation

### Option 1: HACS (Recommended)

1. Add this repository to HACS.
2. Search for "Chore Helper" under "Integrations".
3. Install the integration.
4. Restart Home Assistant.

### Option 2: Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `chore_helper`.
4. Download _all_ the files from the `custom_components/chore_helper/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant.


## Configuration

All configuration is done in the UI.

1. In the HA UI go to "Settings" -> "Devices & Services" -> "Helpers", click the "Create Helper" button, and search for Chore
2. Enter your chore details and submit to add the helper.

## Scheduling

### Chore Calendar

The Chore Helper component creates a calendar that you can add to your calendar view. This calendar will show all of your chores and their due dates. You can also use this calendar to create automations that trigger when a chore is due. For example, you could create an automation that sends you a notification when a chore is due.

The calendar estimates future due dates beyond the next one, which are accurate for "every" tasks but will likely change for "after" tasks depending on when you complete prior chores, as you'll see in the next section.

### Every vs After

Chores that schedule themselves use the prefix of either "after" or "every", and the distinction may seem slight but it can make a big difference in your chore schedule.

Chores that use the "every" prefix are always scheduled based on your start date of the chore. For example, if you start a monthly chore in January and you choose a period of 6 months, then your chore will always be in January and July. If you complete the chore in March, your next due date will still be in July because that is 6 months from the previous due date.

This is perfect for chores that depend on happening on certain days/weeks/months/years, but it's not ideal for many common chores. If you just cleaned the oven 3 days ago, but today is your scheduled oven cleaning day, you're likely not going to clean the oven again. If it's a monthly chore, then you probably aren't going to clean it for another month, right?

That's where the "after" prefix comes in. With an "after" chore, once you've completed it at least one time, it's then always scheduled based on the date you last completed it. Let's take the same example from last time: you start a monthly chore in January and choose a period of 6 months. If you complete the chore in March, then your next due date will be in September, and not July.

"After" chores are perfect for most types of cleaning. Even cleaning chores that should only happen during certain seasons work well with "after" periods because you can choose starting and ending months that will always be in effect. For example, you could configure a chore to mow the lawn every 2 weeks on Saturday between the months of April and November, and the next chore will always be on the Saturday that occurs at least 2 weeks since you last mowed the lawn.

### Time Period Options

The time periods are daily, weekly, monthly, yearly, and custom. All of the options except custom allow entering a numeric period of the selected units (e.g. 7 days, 1 week, 6 months, etc...). The time periods other than yearly and custom can also be configured with starting and ending months each year. Custom chores do not schedule any due dates automatically, allowing you to call a service to schedule the next chore date however you'd like.

Daily chores simply get scheduled to occur every day, or every N days.

Weekly chores can be scheduled to occur on certain days of the week, or the weekdays can be left blank if you just want it to happen every 2 weeks regardless of the day.

Monthly chores can be scheduled in several ways based on the options you choose:
- On a certain day each due month
- On the Nth chosen weekday of the month
- On the chosen weekday of the Nth week of the month
- With none of the options chosen, it will simply be due on the first possible day of the next due month

Yearly chores are scheduled to occur on a certain day and month each year, or every N years.

### Chore Attributes

The main state value for a chore is the number of days until (or since) the next due date. If the due date is in the future, the number will be positive. If the due date is in the past, the number will be negative. If the due date is today, the number will be 0. You can choose different icons for future chores, chores due tomorrow, chores due today, and overdue chores.

The other attributes are the next due date, the last completed date, whether the chore is overdue, and the number of days overdue.

### Person Allocation

Chore Helper integrates with Home Assistant's Person entities to assign chores to specific people in your household. There are four allocation modes:

1. **None** - No person allocation. The chore is not assigned to anyone specifically.

2. **Single** - Assign the chore to one specific person. The chore will always be assigned to this person.

3. **Alternating** - Assign the chore to people in rotation. Each time the chore is completed, it will automatically rotate to the next person in the list. This is perfect for chores that should be shared among household members.

4. **Shared** - The chore appears in everyone's list. This is useful for chores that anyone can complete, or chores that require everyone's participation.

#### Configuring Person Allocation

1. First, ensure you have created Person entities in Home Assistant (Settings → People)
2. When creating or editing a chore, select the desired allocation mode
3. If you choose "Single", "Alternating", or "Shared", select people from the "People" dropdown
   - You can select multiple people for "Alternating" and "Shared" modes
   - For "Single" mode, select one person (the first person in your selection will be used)
4. For "Single" mode, the chore will always be assigned to the selected person
5. For "Alternating" mode, the chore starts with the first person and rotates through the list each time it's completed
6. For "Shared" mode, the chore appears for all selected people

#### Person Attributes

The chore sensor exposes the following person-related attributes:
- `assigned_to`: The entity_id of the currently assigned person (e.g., `person.john`)
- `assigned_to_name`: The friendly name of the currently assigned person (displayed as a chip in the UI)
- `people`: List of person entity_ids configured for this chore
- `allocation_mode`: The allocation mode (none, single, alternating, or shared)

## Services

### chore_helper.complete

This service can be called to mark a chore as completed. It will automatically schedule the next due date for the chore, and adjust future due dates if necessary (e.g. when scheduling "after" chores). For chores with alternating person allocation, this will automatically rotate to the next person in the list.

| Service Data Attribute | Optional | Description                                                                             |
| ---------------------- | -------- | --------------------------------------------------------------------------------------- |
| `entity_id`            | No       | The entity ID of the chore or chores to complete.                                       |
| `last_completed`       | Yes      | The date the chore was last completed. If not specified, the current date will be used. |

### chore_helper.add_date

This service can be called to add a due date to a chore manually. This is useful for custom chores that don't have any due dates scheduled automatically.

| Service Data Attribute | Optional | Description                                                |
| ---------------------- | -------- | ---------------------------------------------------------- |
| `entity_id`            | No       | The entity ID of the chore or chores to add a due date to. |
| `date`                 | No       | The date the chore is due.                                 |

### chore_helper.offset_date

This service can be called to offset the next due date of a chore. This will only affect the next due date for "every" chores, but will affect all future due dates for "after" chores since they are fluid and based on the previous date.

| Service Data Attribute | Optional | Description                                                                     |
| ---------------------- | -------- | ------------------------------------------------------------------------------- |
| `entity_id`            | No       | The entity ID of the chore or chores to offset the due date of.                 |
| `offset`               | No       | The number of days to offset the due date by. This can be positive or negative. |
| `date`                 | Yes      | The date of the chore to offset, or the next due date if blank.                 |

### chore_helper.remove_date

This service can be called to remove a chore date (e.g. skip a chore). This removes the next due date if no date is passed. If a date is passed, it will remove the due date that matches the date passed. Even if no due date currently matches, the removal will persist so that if a due date is added that matches the date passed, it will be removed as well.

| Service Data Attribute | Optional | Description                                                     |
| ---------------------- | -------- | --------------------------------------------------------------- |
| `entity_id`            | No       | The entity ID of the chore or chores to add a due date to.      |
| `date`                 | Yes      | The date of the chore to remove, or the next due date if blank. |

### chore_helper.update_state

This service can be called to update the state of a chore. This is mainly useful for custom chores that don't automatically update themselves.

### chore_helper.get_chores_by_person

This service can be called to get all chores assigned to a specific person. It returns chores that are either:
- Assigned to the person in single or alternating mode
- Configured as shared and the person is in the people list

| Service Data Attribute | Optional | Description                                                   |
| ---------------------- | -------- | ------------------------------------------------------------- |
| `person`               | No       | The entity_id of the person entity (e.g., `person.john`).     |

The service returns a dictionary with a `chores` key containing a list of matching chores with their details including name, due date, allocation mode, and assigned person name.

Example usage in an automation:
```yaml
service: chore_helper.get_chores_by_person
data:
  person: person.john
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[buymecoffee]: https://www.buymeacoffee.com/benmcclure
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/bmcclure/ha-chore-helper.svg?style=for-the-badge
[commits]: https://github.com/bmcclure/ha-chore-helper/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Ben%20McClure%20%40bmcclure-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/bmcclure/ha-chore-helper.svg?style=for-the-badge
[releases]: https://github.com/bmcclure/ha-chore-helper/releases
