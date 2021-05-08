import argparse
import json
import logging
import os
from math import sin, cos, acos, radians

import folium

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

OFFICE = {
    "latitude": "53.339428",
    "longitude": "-6.257664",
    "name": "Dublin Office"
}


def get_absolute_longitude(a1, a2):
    delta = float(a2['longitude']) - float(a1['longitude'])
    return abs(delta)


def calculate_distance(source, dest):
    r = 6371
    source_lat_rads = radians(float(source['latitude']))
    dest_lat_rads = radians(float(dest['latitude']))
    abs_long_rad = radians(get_absolute_longitude(source, dest))
    sin_p = sin(source_lat_rads) * sin(dest_lat_rads)
    cos_p = cos(source_lat_rads) * cos(dest_lat_rads) * cos(abs_long_rad)
    c_angle = acos(sin_p + cos_p)
    distance = round(r * c_angle)
    return distance


def read_file(file):
    with open(file, "r") as file_obj:
        data = file_obj.readlines()
    return data


def save_customers(customers, output):
    with open(output, 'w') as file:
        for customer in customers:
            content = {
                "name": customer['name'],
                "user_id": customer['user_id']
            }
            file.write(json.dumps(content) + "\n")


def search_customers(input, radius):
    logging.debug(f'input={input}, radius={radius}')
    found_customers = []
    if os.path.isfile(input):
        data = read_file(input)
        if data:
            for line in data:
                customer = json.loads(line)
                distance = calculate_distance(OFFICE, customer)
                if distance <= radius:
                    found_customers.append(customer)
    else:
        logging.error("File not found!")
    return found_customers


def sort_customers_by_user_id(customers):
    customers.sort(key=lambda customer: customer['user_id'])


def plot(customers, radius):
    office = float(OFFICE['latitude']), float(OFFICE['longitude'])
    m = folium.Map(location=office)

    folium.Marker(office, popup=f'<i>Office</i>',
                  icon=folium.Icon(color="red")).add_to(m)

    folium.Circle(
        radius=radius * 1000,
        location=office,
        popup="The office",
        color="#3186cc",
        fill_color="#3186cc",
        fill=True
    ).add_to(m)

    for customer in customers:
        folium.Marker([customer['latitude'], customer['longitude']], popup=f"<i>{customer['name']}</i>",
                      icon=folium.Icon(color="green")).add_to(m)
    m.save(f'customers_within_{radius}_km.html')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="Input customer data")
    parser.add_argument("--output", type=str, default="output.txt", required=False, help="output file name")
    parser.add_argument("--radius", type=float, metavar="RADIUS", default=100, required=False,
                        help="Radius to search")
    parser.add_argument("--plot", action="store_true", required=False)

    args = parser.parse_args()

    customers = search_customers(args.input, args.radius)
    if customers:
        logging.info(f'Found {len(customers)} customers within {args.radius} km radius')
        sort_customers_by_user_id(customers)
        save_customers(customers, output=args.output)
        if args.plot:
            plot(customers, args.radius)
    else:
        logging.info(f'No customers found within {args.radius} km radius.')
