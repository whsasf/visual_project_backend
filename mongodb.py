from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['bito']

# bitoc: store China city map data
# bitoct1: store latest random array data
# bitoct2: store total random array data ,is a Capped Collections ,max: 700

def mongodbinit():
    collist = db.list_collection_names()
    if "bitoc" in collist:
        print("bitoc集合已存在")
    else:
        print("bitoc集合未存在")
        collection = db['bitoc']
        # read city data of China
        with open('./static/cityData.json',encoding='utf-8') as f:
            cityData = json.loads(f.read())

        # inset city data of China
        try:
            collection.insert_many(cityData)
        except Exception as e:
            print("插入cityData发生错误 : " + e)

    # check if Capped Collections exist
    if 'bitoct2' in collist:
        print('bitoct2 Capped Collections 存在')
    else:
        print('bitoct2 Capped Collections 不存在')
        # 创建
        try:
            db.create_collection('bitoct2', capped=True, max=700,size=300,codec_options=None)
        except Exception as e:
            print(e)


async def get_random_lines(N):
    random_lines = db['bitoc'].aggregate( [ { "$sample": { "size": N }}, {"$project": {"_id": 0 }}] )
    return list(random_lines)


async def insert_many(datalists):
    try:
        #1- empty bitoct1 firstly
        db['bitoct1'].drop()
        #2- add new data
        db['bitoct1'].insert_many(datalists)
    except Exception as e:
        return (e)
    return None

async def insert_many_t2(datalists):
    try:
        #2- sum new data
        db['bitoct2'].insert_many(datalists)
    except Exceptions as e:
        return (e)
    return None


async def get_t2_lines(lines_bumber):
    xdata = list(db['bitoct2'].find().sort('_id',-1).limit(lines_bumber))
    for ele in xdata:
        ele.pop('_id')
    return xdata