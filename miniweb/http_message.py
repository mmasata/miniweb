#trida obalujici HTTP request
class Request:

    def __init__(self):
        print("Miniweb dostal request...")


    #prijata data jsou RAW, je treba je roztridit
    async def parse(self, data):
        #data prijdou v bytech, je treba je precodovat
        row_arr = data.decode().split("\r\n")
        row_arr_len = len(row_arr)
        read_content = False
        content_len = content_len_read = 0
        self.content = ""
        for i in range(0, row_arr_len):
            if i == 0:
                #na zacatku dostaneme metodu, cestu a protokol
                self.method, full_path, self.protocol = row_arr[i].split()
                await self.find_query_params(full_path)
                continue
            if "Content-Type:" in row_arr[i] and not read_content:
                self.type = row_arr[i].split()[1]
                continue
            if "Content-Length:" in row_arr[i] and not read_content:
                content_len = int(row_arr[i].split()[1])
                print(content_len)
                read_content = True
                continue
            if read_content:
                #kontrolujeme zda jeste muzeme cist
                content_len_read += len(row_arr[i])
                if content_len_read <= content_len:
                    self.content += row_arr[i]
                    #pokud mame jiz vsechny radky, necteme dale
                    if content_len == content_len_read:
                        read_content = False


    #z cesty si vytahne query params a ulozi je do dictionary
    async def find_query_params(self, full_path):
        if "?" in full_path:
            self.path, q_par_str = full_path.split("?", 1)
            q_par_arr = q_par_str.split("&")
            self.params = {}
            for par in q_par_arr:
                key, value = par.split("=")
                self.params[key] = value
        else:
            self.path = full_path


#trida obalujici HTTP response
class Response:

    def __init__(self):
        self.can_send = False


    #ulozi do instance status kod responsu
    def status(self, status):
        self.status = status
        return self

    #ulozi do promenne data, ktera bude vracet v response
    def entity(self, data):
        self.entity = data
        return self

    #ulozi do promenne mime type, ktery bude response vracet
    def type(self, mime):
        self.type = mime
        return self

    #zmeni boolean parametr na True, tim da najevo ze je response hotova k vraceni
    def build(self):
        self.can_send = True
        return self
