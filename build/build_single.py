from shabbypipeline import get_pipeline

files = random.sample(os.listdir(), 100)

def shabbify(f):
    if "png" in f:
        img = cv2.imread(f)
        pipeline = get_pipeline()
        out_path = "out/" + f[:-4] + "-augraphy.png"
        augmented = pipeline.augment(img)["output"]
        # make it all grayscale again in case we used a paper texture
        crappified = cv2.cvtColor(crappified, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(crappified_path, crappified)

p = Pool(32)

p.map(crappify, files)
