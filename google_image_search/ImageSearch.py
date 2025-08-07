import json
import os

from serpapi import GoogleSearch
from content_generator.helper.ImageConfig import ImageConfig

class ImageSearch:


  def search(self,search_txt):

      print("Searching the characters on internet to get the images..")

      search_txt = search_txt[:3]
      image_results = []
      full_paths = []


      for search in search_txt:
          params = {
              "api_key": os.getenv("GOOGLE_API_KEY"),
              "engine": "google",
              "q": "recent picture of "+search,
              "google_domain": "google.com",
              "tbm": "isch",
              "nfpr": "1",
              "ijn": 0,
              "num": "10"  # fetch up to 10, but we’ll stop at 4 manually
          }

          search_api = GoogleSearch(params)
          images_is_present = True
          images_collected = 0  # Track count per search term

          while images_is_present and images_collected < 4:
              results = search_api.get_dict()

              if "error" not in results:
                  for image in results.get("images_results", []):
                      if image["original"] not in image_results:
                          image_results.append(image["original"])
                          image_path_data = ImageConfig.download_images(image["original"],search)
                          if image_path_data != "" :
                              full_paths.append(image_path_data)

                          images_collected += 1

                          if images_collected >= 4:
                              break  # Stop once 4 images are collected

                  params["ijn"] += 1  # next page
                  search_api = GoogleSearch(params)  # re-initialize with updated params
              else:
                  images_is_present = False
                  print(results["error"])

     #data = json.dumps(image_results, indent=2)
      print(full_paths)
      return full_paths




