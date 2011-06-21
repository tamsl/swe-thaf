while 1:
    data = s.recv(BUFFER_SIZE)
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        string = data.split('\r\n')
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
                if len(datasplit) > 0:
                    # Sensor message
                    if datasplit[0] == "SEN":
                        typeSEN = datasplit[1].replace('{Type ', '')
                        typeSEN = typeSEN.replace('}', '')
                        if len(datasplit) > 2:
                            typeSEN2 = datasplit[2].replace('{Type ', '')
                            typeSEN2 = typeSEN2.replace('}', '')
                        if typeSEN2 == "RangeScanner":
                            #datasplit[6] bevat data
                        if typeSEN == "Odometry":
                            #geen idee
