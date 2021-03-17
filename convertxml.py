
import xml.dom.minidom as md
import re
#Import file and export file


def import_xml(import_file):
    data = md.parse(import_file)
    return data



def tablefy(data):
    #Turns xml into somthing we can easily process

    data_table = []
    rows = data.getElementsByTagName("ROW")

    for row in rows:
        cols = row.getElementsByTagName("DATA")
        temp_list = [row.getAttribute("RECORDID")]
        for col in cols:
           temp_list.append(col.firstChild.nodeValue)
        data_table.append(temp_list)
    col_names = ["ID"]
    for field in data.getElementsByTagName("FIELD"):
        col_names.append(field.getAttribute("NAME"))
    return col_names, data_table



#Writing the data to a new xml file that access can read
def  accessify(table, data, export_file):
    lines= []
    names = table[0]
    for i in range(len(names)):
	    names[i] = re.sub(" ", "_x0020_", names[i])
    
    entries = table[1]

    db_name = data.getElementsByTagName("DATABASE")[0].getAttribute("NAME")
    db_name = re.sub(".fp7", "", db_name)

    #Header
    lines.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    lines.append("<dataroot xmlns:od=\"urn:schemas-microsoft-com:officedata\" generated=\"2021-03-16T16:17:17\">")
    
    #Entries
    for i in range(len(entries)):
        entry = entries[i]
        #<[name]>
        lines.append("<"+db_name+">")
        for j in range(len(entry)):
            line = "<"+names[j]+">"+entry[j]+"</"+names[j]+">"
            lines.append(line)
        #</[name]>
        lines.append("</"+db_name+">")

    #Footer
    lines.append("</dataroot>")

    export = open(export_file, "w")
    export.writelines(lines)
    export.close()







def main():
    import_file = "fmpro1.xml"
    export_file = "test.xml"
    data = import_xml(import_file)
    table = tablefy(data)
    accessify(table, data, export_file)


    

main()