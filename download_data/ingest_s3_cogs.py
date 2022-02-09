import boto3
import json, os
import pickle
from botocore.handlers import disable_signing

resource = boto3.resource('s3')
resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    
bucket = resource.Bucket('sentinel-cogs')
collectionName = 'sentinel-s2-l2a-cogs'
count = 0
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

            features.append(data)
    
    except Exception as e:
        print(e)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

with open(f'{collectionName}.json', 'wb') as fp:
    pickle.dump(feature_collection, fp)