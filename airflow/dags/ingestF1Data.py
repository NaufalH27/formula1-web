from helper.jsonHelper import get_value


def get_race_info_data():
    race_info = None
    return race_info

def get_participant_data():
    race_data = None
    qualifying_data = None
    sprint_data = None

    qualifying_results = get_value(qualifying_data,"Races", 0, "QualifyingResults") or []
    sprint_results = get_value(sprint_data, "Races", 0, "SprintResults") or []
    race_results =  get_value(race_data,"Races", 0, "Results") or []
    participant_list = qualifying_results + sprint_results + race_results
    processed_participant = []
    unique_participant = set()

    for element in participant_list:
        driver_ref = get_value(element, "Driver", "driverId")
        driver_number = get_value(element, "number") or "0"

        if (driver_ref, driver_number) not in unique_participant:
            unique_participant.add((driver_ref, driver_number))
            processed_participant.append(element)
        else:
            continue
    return processed_participant

def get_race_result_data():
    race_data = None
    return get_value(race_data, "Races", 0, "Results")

def get_qualifying_result_data():
    qualifying_data = None
    return get_value(qualifying_data, "Races", 0, "QualifyingResults")

def get_sprint_data():
    sprint_data = None
    return get_value(sprint_data, "Races", 0, "SprintResults")

    