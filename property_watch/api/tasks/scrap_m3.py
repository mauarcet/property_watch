import requests
from bs4 import BeautifulSoup
from api.utils.normalizers import normalize_li_tags, normalize_price, normalize_address, normalize_size
from api.models import Property, PropertyAmenity, PropertyDescription


class ScrapperM3:
    def __init__(self, base_url, limit):
        self.base_url = base_url
        self.limit = limit

    def get_links_to_crawl(self, base_url, limit):
        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, "html.parser")
        list_of_properties = soup.find(id="searchResults").find_all(
            "li", class_=False, limit=limit
        )
        links_per_page = len(list_of_properties)
        property_links = []
        for property_ in list_of_properties:
            property_links.append(property_.a.get("href"))

        while len(property_links) < limit:
            limit_remained = limit - len(property_links)
            next_page = soup.find("a", class_="andes-pagination__link prefetch").get(
                "href"
            )
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, "html.parser")
            list_of_properties = soup.find(id="searchResults").find_all(
                "li", class_=False, limit=limit_remained
            )
            for property_ in list_of_properties:
                property_links.append(property_.a.get("href"))

        print(f"All {len(property_links)} links obtained!")
        return property_links

    def write_properties_on_db(self, links_to_crawl):
        collected_data = []
        for iterator, property_url in enumerate(links_to_crawl):
            property_page = requests.get(property_url)
            property_soup = BeautifulSoup(property_page.text, "html.parser")
            property_name = property_soup.find(
                "div", class_="vip-product-info__development__info"
            ).h1.text
            property_full_address = property_soup.find("h2", class_="map-location").text
            property_first_image = (
                property_soup.find("div", id="short-description-gallery")
                .ul.find("li")
                .img.get("src")
            )
            property_price = (
                property_soup.find("div", class_="vip-product-info__development__info")
                .find("strong")
                .text
            )
            property_size = (
                property_soup.find("section", class_="vip-product-info__attributes")
                .ul.find("li")
                .find("span")
                .text
            )
            amenities_tag = property_soup.find("ul", class_="boolean-attribute-list")
            if amenities_tag:
                amenities = amenities_tag.find_all("li")
                property_amenities = normalize_li_tags(amenities)
            else:
                property_amenities = ""
            property_description = property_soup.find(
                "pre", class_="preformated-text"
            ).text
            # Create elements in DB
            try:
                property = Property.objects.get(name=property_name)
            except:
                property = None
            if property is None:
                norm_address = normalize_address(property_full_address)
                property = Property(
                    name=property_name,
                    price=str(normalize_price(property_price)),
                    street_name=norm_address['street_name'],
                    street_number=norm_address['street_number'],
                    settlement=norm_address['settlement'],
                    town=norm_address['town'],
                    state=norm_address['state'],
                    country=norm_address['country'],
                    size=str(normalize_size(property_size)),
                    image=property_first_image,
                )
                try:
                    property.save()
                    print(f"Property {property_name} added to DB")                
                except:
                    print("Error: Property not saved ----------------")
                    print(f"{property_name}")
                    print(f"{property_price}")
                    print(f"{property_size}")
                    print(f"{property_full_address}")
                    print(f"{property_first_image}")
                    print("------------------------------------------")
        print("All new properties were added to de the DB")

    def run(self):
        links_to_crawl = self.get_links_to_crawl(self.base_url, self.limit)
        self.write_properties_on_db(links_to_crawl)
