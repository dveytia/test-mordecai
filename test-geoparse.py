from mordecai import Geoparser
print("imported Geoparser")
geo = Geoparser()
loc = geo.geoparse("I went from Oxford to Ottawa")
print(loc)
