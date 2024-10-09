import sys,os
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get_item(self, key: str) -> str:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def set_item(self, key: str, value: str) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)


yeardir = sys.argv[1]
TM_type = sys.argv[2]

rootdir = sys.argv[1]+ sys.argv[2]


maxsize=1000
d = LRUCache(maxsize)
c = 0


fw = open(sys.argv[3]+".revisit", "w")

for filename in os.listdir(rootdir):
	if filename.startswith('TM_'):
		#fw22 = open(sys.argv[1]+"/TM_2022/"+ filename, "w")
		fullfilename = os.path.join(rootdir, filename)
		#print(fullfilename)
		tmpfullfilename = os.path.join(rootdir, "tmp_"+filename)
		ft = open(tmpfullfilename, "w")
		f = open(fullfilename, "r")
		try:
			for line in f:
				c = c+1
				line = line.strip('\n')
				line_l = line.split(" ")
				url = line_l[0]
				mime = line_l[4]
				sc = line_l[5]
				hash_key = line_l[6]
				if mime == 'warc/revisit':
					hydrate_mime, hydrate_sc, old_line_no = d.get_item(hash_key)
					line_l[4] = hydrate_mime
					line_l[5] = hydrate_sc
					line = " ".join(line_l)
					dist = str(c-old_line_no)
					fw.write(filename+"\t"+hash_key+"\t"+dist+"\n")
				else:
					d.set_item(hash_key,(mime,sc,c))
				ft.write(line+"\n")
			os.replace(tmpfullfilename, fullfilename)
			f.close()
			ft.close()
		except:
			print(filename)
			continue
