/* SPDX-License-Identifier: GPL-3.0-or-later
 * Board vesc4_12B02, SCH_SchematicV01_2_2026-10-19.pdf.
 * Commissioning configuration, not a validated production power rating.
 */
#ifndef HW_DRV8302_B02_H_
#define HW_DRV8302_B02_H_
#define HW_SOURCE_ALT "other/vesc4/hw_410.c"
#define CURRENT_SHUNT_RES 0.0005
#define CURRENT_AMP_GAIN 10.0
#define VIN_R1 39000.0
#define VIN_R2 2200.0
#define MCCONF_L_CURRENT_MAX 5.0
#define MCCONF_L_CURRENT_MIN -2.0
#define MCCONF_L_IN_CURRENT_MAX 2.0
#define MCCONF_L_IN_CURRENT_MIN -0.5
#define MCCONF_L_MAX_ABS_CURRENT 10.0
#define MCCONF_L_MIN_VOLTAGE 10.0
#define MCCONF_L_MAX_VOLTAGE 30.0
#define MCCONF_L_BATTERY_CUT_START 11.0
#define MCCONF_L_BATTERY_CUT_END 10.0
#define MCCONF_L_RPM_MAX 10000.0
#define MCCONF_L_RPM_MIN -10000.0
#define MCCONF_L_MAX_DUTY 0.2
#define MCCONF_L_WATT_MAX 50.0
#define MCCONF_L_WATT_MIN -10.0
#define MCCONF_L_LIM_TEMP_FET_START 60.0
#define MCCONF_L_LIM_TEMP_FET_END 75.0
#define APPCONF_APP_TO_USE APP_NONE
#define APPCONF_TIMEOUT_MSEC 1000
#define APPCONF_TIMEOUT_BRAKE_CURRENT 0.0
#include "hw_410.h"
#undef HW_NAME
#define HW_NAME "DRV8302_B02"
/* R30: 10 kohm B3450 high-side NTC; R31: 10 kohm to ground. */
#undef NTC_TEMP
#define NTC_TEMP(adc_ind) (1.0 / ((logf(NTC_RES(ADC_Value[adc_ind]) / 10000.0) / 3450.0) + (1.0 / 298.15)) - 273.15)
#endif
