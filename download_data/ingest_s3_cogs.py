import boto3
import json, os
import pickle
from botocore.handlers import disable_signing

resource = boto3.resource('s3')
resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    
bucket = resource.Bucket('sentinel-cogs')
collectionName = 'sentinel-s2-l2a-cogs'
init_count = 210001
count = 0
final_count = 300000
features = []

for item in bucket.objects.all():
    try:
        tag = item.key[-4:]
        if(tag=='json'):
            split = item.key.split('/')
            passYear = split[1]
            passYear = int(passYear)
            if(passYear < 2000):
                location = split[7]
            else:
                location = split[3]
            id = location[:-5]
            print('id: ', id)
            count +=1
            print('count:', count)

            if count >= init_count:
                bucket.download_file(item.key, location)
                print('add')
                # item.save(item.id + '.json')
                with open(id + '.json') as f:
                    data = json.load(f)
                os.remove(id + '.json')

                self = "http://discovery-cosmos.azurewebsites.net/stac/collections/" + collectionName + "/items/" + id
                parent = "http://discovery-cosmos.azurewebsites.net/stac/collections/" + collectionName
                collection = "http://discovery-cosmos.azurewebsites.net/stac/collections/" + collectionName
                root = "http://discovery-cosmos.azurewebsites.net/stac/"
                title = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items/" + id
                canonical = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/" + item.key

                data["links"] = [{"rel": "self", "href": self},
                    #{"rel": "canonical", "href": "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/15/S/VS/2017/11/S2A_15SVS_20171110_1_L2A/S2A_15SVS_20171110_1_L2A.json", "type": "application/json"},
                    {"rel": "canonical", "href": canonical, "type": "application/json"},
                    {"title": "Source STAC Item", "rel": "derived_from", "href": title, "type": "application/json"},
                    {"rel": "parent", "href": parent},
                    {"rel": "collection", "href": collection},
                    {"rel": "root", "href": root}]

                data["version"] = "1.0.0"

                features.append(data)

            if count==final_count:
                break
    
    except Exception as e:
        print(e)

feature_collection = {
    "type": "FeatureCollection",
    "features": features
}

path = 'stac_fastapi_loader/test_data/sentinel_data/'

path_exists = os.path.exists(path)

if not path_exists:
  os.makedirs(path)

file_name = f"{path}{collectionName}_{init_count}_{final_count}.json"

with open(file_name, 'w') as fp:
    json.dump(feature_collection, fp)