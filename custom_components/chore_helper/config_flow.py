"""Adds config flow for Chore Helper."""

from __future__ import annotations

# import uuid
from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol
from homeassistant.const import ATTR_HIDDEN, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowError,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
    SchemaOptionsFlowHandler,
)

from . import const, helpers


async def _validate_config(
    _: SchemaConfigFlowHandler | SchemaOptionsFlowHandler, data: Any
) -> Any:
    """Validate config."""
    # Map new pattern-based recurrence to legacy frequency (if using new system)
    if const.CONF_RECURRENCE_TYPE in data:
        recurrence_type = data[const.CONF_RECURRENCE_TYPE]

        if recurrence_type == "daily":
            pattern = data.get(const.CONF_DAILY_PATTERN, "every_n_days")
            if pattern == "every_n_days":
                data[const.CONF_FREQUENCY] = "every-n-days"
            elif pattern == "every_weekday":
                data[const.CONF_FREQUENCY] = "every-n-days"
                data[const.CONF_PERIOD] = 1  # Every 1 day, but only weekdays
                # TODO: Need backend support for weekday filtering
            elif pattern == "regenerate_days":
                data[const.CONF_FREQUENCY] = "after-n-days"

        elif recurrence_type == "weekly":
            pattern = data.get(const.CONF_WEEKLY_PATTERN, "recur_weekly")
            if pattern == "recur_weekly":
                data[const.CONF_FREQUENCY] = "every-n-weeks"
            elif pattern == "regenerate_weeks":
                data[const.CONF_FREQUENCY] = "after-n-weeks"

        elif recurrence_type == "monthly":
            pattern = data.get(const.CONF_MONTHLY_PATTERN, "day_of_month")
            if pattern in ["day_of_month", "nth_day_type"]:
                data[const.CONF_FREQUENCY] = "every-n-months"
            elif pattern == "regenerate_months":
                data[const.CONF_FREQUENCY] = "after-n-months"

        elif recurrence_type == "yearly":
            pattern = data.get(const.CONF_YEARLY_PATTERN, "month_day")
            if pattern in ["month_day", "nth_day_type_of_month"]:
                data[const.CONF_FREQUENCY] = "every-n-years"
            elif pattern == "regenerate_years":
                data[const.CONF_FREQUENCY] = "after-n-years"

    if const.CONF_DAY_OF_MONTH in data and data[const.CONF_DAY_OF_MONTH] < 1:
        data[const.CONF_DAY_OF_MONTH] = None

    if const.CONF_DATE in data:
        if (
            data[const.CONF_DATE] == "0"
            or data[const.CONF_DATE] == "0/0"
            or data[const.CONF_DATE] == ""
        ):
            data[const.CONF_DATE] = None
        else:
            try:
                helpers.month_day_text(data[const.CONF_DATE])
            except vol.Invalid as exc:
                raise SchemaFlowError("month_day") from exc

    if (
        const.CONF_WEEKDAY_ORDER_NUMBER in data
        and int(data[const.CONF_WEEKDAY_ORDER_NUMBER]) == 0
    ):
        data[const.CONF_WEEKDAY_ORDER_NUMBER] = None

    if const.CONF_CHORE_DAY in data and data[const.CONF_CHORE_DAY] == "0":
        data[const.CONF_CHORE_DAY] = None

    # Validate range of recurrence
    end_type = data.get(const.CONF_END_TYPE, const.DEFAULT_END_TYPE)

    if end_type == "end_by_date":
        if not data.get(const.CONF_END_DATE):
            raise SchemaFlowError("end_date_required")
        # Clear the other end option
        data[const.CONF_END_AFTER_OCCURRENCES] = None
    elif end_type == "end_after_occurrences":
        if not data.get(const.CONF_END_AFTER_OCCURRENCES):
            raise SchemaFlowError("end_after_occurrences_required")
        # Clear the other end option
        data[const.CONF_END_DATE] = None
    else:  # no_end
        # Clear both end options
        data[const.CONF_END_DATE] = None
        data[const.CONF_END_AFTER_OCCURRENCES] = None

    # Auto-determine allocation mode based on people selection
    people = data.get(const.CONF_PEOPLE, [])
    people_count = len(people) if people else 0

    if people_count == 0:
        # No people selected → none
        data[const.CONF_ALLOCATION_MODE] = "none"
    elif people_count == 1:
        # One person selected → single
        data[const.CONF_ALLOCATION_MODE] = "single"
    else:
        # Multiple people selected → require mode selection
        multiple_mode = data.get(const.CONF_MULTIPLE_PEOPLE_MODE)
        if not multiple_mode:
            raise SchemaFlowError("multiple_people_mode_required")
        data[const.CONF_ALLOCATION_MODE] = multiple_mode

    return data


def required(
    key: str, options: dict[str, Any], default: Any | None = None
) -> vol.Required:
    """Return vol.Required."""
    if isinstance(options, dict) and key in options:
        suggested_value = options[key]
    elif default is not None:
        suggested_value = default
    else:
        return vol.Required(key)
    return vol.Required(key, description={"suggested_value": suggested_value})


def optional(
    key: str, options: dict[str, Any], default: Any | None = None
) -> vol.Optional:
    """Return vol.Optional."""
    if isinstance(options, dict) and key in options:
        suggested_value = options[key]
    elif default is not None:
        suggested_value = default
    else:
        return vol.Optional(key)
    return vol.Optional(key, description={"suggested_value": suggested_value})


async def step_details_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Step 1: Chore Details - Name and Icon."""
    schema = {}
    options = handler.options if hasattr(handler, 'options') else {}

    schema[required(CONF_NAME, options)] = selector.TextSelector()
    schema[optional(const.CONF_ICON, options, const.DEFAULT_ICON)] = (
        selector.IconSelector()
    )

    return vol.Schema(schema)


async def step_recurrence_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Step 2: Recurrence Pattern - Show only relevant fields based on type."""
    schema = {}
    options = handler.options if hasattr(handler, 'options') else {}

    # Recurrence type selector
    schema[optional(const.CONF_RECURRENCE_TYPE, options, const.DEFAULT_RECURRENCE_TYPE)] = (
        selector.SelectSelector(
            selector.SelectSelectorConfig(options=const.RECURRENCE_TYPE_OPTIONS)
        )
    )

    # Get current recurrence type
    recurrence_type = options.get(const.CONF_RECURRENCE_TYPE, const.DEFAULT_RECURRENCE_TYPE)

    # Show pattern fields based on recurrence type
    if recurrence_type == "daily":
        schema[optional(const.CONF_DAILY_PATTERN, options, "every_n_days")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.DAILY_PATTERN_OPTIONS)
            )
        )

    elif recurrence_type == "weekly":
        schema[optional(const.CONF_WEEKLY_PATTERN, options, "recur_weekly")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.WEEKLY_PATTERN_OPTIONS)
            )
        )
        schema[optional(const.CONF_WEEKLY_DAYS, options, [])] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(value="mon", label="Monday"),
                        selector.SelectOptionDict(value="tue", label="Tuesday"),
                        selector.SelectOptionDict(value="wed", label="Wednesday"),
                        selector.SelectOptionDict(value="thu", label="Thursday"),
                        selector.SelectOptionDict(value="fri", label="Friday"),
                        selector.SelectOptionDict(value="sat", label="Saturday"),
                        selector.SelectOptionDict(value="sun", label="Sunday"),
                    ],
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            )
        )

    elif recurrence_type == "monthly":
        schema[optional(const.CONF_MONTHLY_PATTERN, options, "day_of_month")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.MONTHLY_PATTERN_OPTIONS)
            )
        )
        schema[optional(const.CONF_DAY_TYPE, options, "day")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.DAY_TYPE_OPTIONS)
            )
        )

    elif recurrence_type == "yearly":
        schema[optional(const.CONF_YEARLY_PATTERN, options, "month_day")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.YEARLY_PATTERN_OPTIONS)
            )
        )
        schema[optional(const.CONF_DAY_TYPE, options, "day")] = (
            selector.SelectSelector(
                selector.SelectSelectorConfig(options=const.DAY_TYPE_OPTIONS)
            )
        )

    # Period for all types
    schema[optional(const.CONF_PERIOD, options, const.DEFAULT_PERIOD)] = (
        selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=1000,
                mode=selector.NumberSelectorMode.BOX,
            )
        )
    )

    return vol.Schema(schema)


async def step_range_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Step 3: Range of Recurrence - Start/End dates."""
    schema = {}
    options = handler.options if hasattr(handler, 'options') else {}

    # Start date
    schema[optional(const.CONF_START_DATE, options, helpers.now().date())] = (
        selector.DateSelector()
    )

    # End type selector
    schema[optional(const.CONF_END_TYPE, options, const.DEFAULT_END_TYPE)] = (
        selector.SelectSelector(
            selector.SelectSelectorConfig(options=const.END_TYPE_OPTIONS)
        )
    )

    # Get current end type
    end_type = options.get(const.CONF_END_TYPE, const.DEFAULT_END_TYPE)

    # Show only relevant end field
    if end_type == "end_by_date":
        schema[optional(const.CONF_END_DATE, options)] = (
            selector.DateSelector()
        )
    elif end_type == "end_after_occurrences":
        schema[optional(const.CONF_END_AFTER_OCCURRENCES, options)] = (
            selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=1000,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="occurrences",
                )
            )
        )

    # Seasonal chores - first/last month
    schema[optional(const.CONF_FIRST_MONTH, options, const.DEFAULT_FIRST_MONTH)] = (
        selector.SelectSelector(
            selector.SelectSelectorConfig(options=const.MONTH_OPTIONS)
        )
    )
    schema[optional(const.CONF_LAST_MONTH, options, const.DEFAULT_LAST_MONTH)] = (
        selector.SelectSelector(
            selector.SelectSelectorConfig(options=const.MONTH_OPTIONS)
        )
    )

    return vol.Schema(schema)


async def step_allocation_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Step 4: Person Allocation - Assign to people."""
    schema = {}
    options = handler.options if hasattr(handler, 'options') else {}

    # People selector
    schema[optional(const.CONF_PEOPLE, options, [])] = (
        selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain="person",
                multiple=True,
            )
        )
    )

    # Only show mode selector if multiple people
    people = options.get(const.CONF_PEOPLE, [])
    people_count = len(people) if people else 0

    if people_count > 1:
        current_allocation_mode = options.get(const.CONF_ALLOCATION_MODE)
        if current_allocation_mode in ["alternating", "shared"]:
            schema[optional(const.CONF_MULTIPLE_PEOPLE_MODE, options, current_allocation_mode)] = (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(options=const.MULTIPLE_PEOPLE_MODE_OPTIONS)
                )
            )
        else:
            schema[optional(const.CONF_MULTIPLE_PEOPLE_MODE, options)] = (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(options=const.MULTIPLE_PEOPLE_MODE_OPTIONS)
                )
            )

    return vol.Schema(schema)


async def step_advanced_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Step 5: Advanced Options."""
    schema = {}
    options = handler.options if hasattr(handler, 'options') else {}

    schema[optional(const.CONF_FORECAST_DATES, options, const.DEFAULT_FORECAST_DATES)] = (
        selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                max=100,
                mode=selector.NumberSelectorMode.BOX,
                step=1,
            )
        )
    )
    schema[optional(ATTR_HIDDEN, options, False)] = bool
    schema[optional(const.CONF_MANUAL, options, False)] = bool
    schema[optional(const.CONF_SHOW_OVERDUE_TODAY, options, const.DEFAULT_SHOW_OVERDUE_TODAY)] = bool

    return vol.Schema(schema)


CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowMenuStep(["details", "recurrence", "range", "allocation", "advanced"]),
    "details": SchemaFlowFormStep(step_details_schema),
    "recurrence": SchemaFlowFormStep(step_recurrence_schema),
    "range": SchemaFlowFormStep(step_range_schema),
    "allocation": SchemaFlowFormStep(step_allocation_schema),
    "advanced": SchemaFlowFormStep(step_advanced_schema, validate_user_input=_validate_config),
}
OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowMenuStep(["details", "recurrence", "range", "allocation", "advanced"]),
    "details": SchemaFlowFormStep(step_details_schema),
    "recurrence": SchemaFlowFormStep(step_recurrence_schema),
    "range": SchemaFlowFormStep(step_range_schema),
    "allocation": SchemaFlowFormStep(step_allocation_schema),
    "advanced": SchemaFlowFormStep(step_advanced_schema, validate_user_input=_validate_config),
}


# mypy: ignore-errors
class ChoreHelperConfigFlowHandler(SchemaConfigFlowHandler, domain=const.DOMAIN):
    """Handle a config or options flow for Chore Helper."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW
    VERSION = const.CONFIG_VERSION

    @callback
    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title.

        The options parameter contains config entry options, which is the union of user
        input from the config flow steps.
        """
        return cast(str, options["name"]) if "name" in options else ""
