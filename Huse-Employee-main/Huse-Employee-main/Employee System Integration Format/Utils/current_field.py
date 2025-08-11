def remove_used_fields_and_return_next(data_object,
                                       mandatory_fields,
                                       optional_personal_fields,
                                       optional_employment_fields,
                                       optional_location_fields):
    for field, value in vars(data_object).items():
        if value is not None and value != "":
            if field in mandatory_fields:
                mandatory_fields.remove(field)
            if field in optional_personal_fields:
                optional_personal_fields.remove(field)
            if field in optional_employment_fields:
                optional_employment_fields.remove(field)
            if field in optional_location_fields:
                optional_location_fields.remove(field)

    if mandatory_fields:
        return "mandatory_fields", mandatory_fields
    elif optional_personal_fields:
        return "optional_personal_fields", optional_personal_fields
    elif optional_employment_fields:
        return "optional_employment_fields", optional_employment_fields
    elif optional_location_fields:
        return "optional_location_fields", optional_location_fields
    else:
        return None, []
    
def remove_fields_by_name_and_return_next(
    used_fields,
    mandatory_fields,
    optional_personal_fields,
    optional_employment_fields,
    optional_location_fields
):
    for field in used_fields:
        if field in mandatory_fields:
            mandatory_fields.remove(field)
        if field in optional_personal_fields:
            optional_personal_fields.remove(field)
        if field in optional_employment_fields:
            optional_employment_fields.remove(field)
        if field in optional_location_fields:
            optional_location_fields.remove(field)

    if mandatory_fields:
        return "mandatory_fields", mandatory_fields
    elif optional_personal_fields:
        return "optional_personal_fields", optional_personal_fields
    elif optional_employment_fields:
        return "optional_employment_fields", optional_employment_fields
    elif optional_location_fields:
        return "optional_location_fields", optional_location_fields
    else:
        return None, []

