import os

import pandas as pd
import numpy as np


def reverseFatContent(row):
    if row['item_fat_content_Low Fat'] == 1:
        val = 'Low_Fat'
    elif row['item_fat_content_Non-Edible'] == 1:
        val = 'Non-Edible'
    elif row['item_fat_content_Regular'] == 1:
        val = 'Regular'
    else: 'Unknown'
    return val


def reverseItemType(row):
    if row['item_type_Drink'] == 1:
        val = 'Drink'
    elif row['item_type_Food'] == 1:
        val = 'Food'
    elif row['item_type_Non-consumable'] == 1:
        val = 'Non-Consumable'
    else: 'Unknown'
    return val

def reverseLocationType(row):
    if row['outlet_location_type_Tier 1'] == 1:
        val = 'Tier-1'
    elif row['outlet_location_type_Tier 2'] == 1:
        val = 'Tier-2'
    elif row['outlet_location_type_Tier 3'] == 1:
        val = 'Tier-3'
    else: 'Unknown'
    return val

def reverseOutletSize(row):
    if row['outlet_size_High'] == 1:
        val = 'High'
    elif row['outlet_size_Medium'] == 1:
        val = 'Medium'
    elif row['outlet_size_Small'] == 1:
        val = 'Small'
    else: 'Unknown'
    return val


def reverseOutletType(row):
    if row['outlet_type_Grocery Store'] == 1:
        val = 'Grocery_Store'
    elif row['outlet_type_Supermarket Type1'] == 1:
        val = 'Supermarket_Type_1'
    elif row['outlet_type_Supermarket Type2'] == 1:
        val = 'Supermarket_Type_2'
    elif row['outlet_type_Supermarket Type3'] == 1:
        val = 'Supermarket_Type_3'
    else: 'Unknown'
    return val