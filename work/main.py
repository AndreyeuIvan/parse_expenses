'''I will try to use xml_to_dict because, I get errors, witch I can not pass. Eqrlier librarie is sucks.'''

''' 1. Take file.
    2. Count tags
    3. Take needfull tags
    4. Get objects
    5. Transform objects into new form.'''

import xmltodict
from datetime import datetime
from collections import OrderedDict

def date_issue(date):
    '''Change date into propriet format'''
    date = date.replace('.','-')
    date = datetime.strptime(date, '%d-%m-%Y')
    date = date.isoformat()[:10]
    return date

def collect_data(file_new):
    '''здесь мы обрабатываем запрос, выделяем объекты и складывем в дикт.
    Перебираем список, пробуем если в дикте 1 объект, то записываем одним образом. Если дикт из нескольких объектов, то записываем иначе, а если никакого, то пропускаем.
    После записываем новый дикт в список и возвращаем его'''
    data_list = []
    #import pdb;pdb.set_trace()
    file = [i for i in file_new if i.get('OPERINFO') != None]
    for i, v in enumerate(file,1):
        try:
            data = OrderedDict()
            try:
                isinstance(v.get('OPERINFO').get('OPER').get('DOCN'),str)
                data['i'] = 0
                data['AccountNumber']=v.get('ACCOUNT')
                data['CurrCode']=v.get('CURRENCY').get('@Code')
                data['Currency'] = v.get('CURRENCY').get('@Iso')
                data['DocumentDate'] = date_issue(v.get('PERIOD')[3:])
                data[1] = {
                                    'doc':v.get('OPERINFO').get('OPER').get('DOCN'),
                                    'nd':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@nd'),
                                    'nk':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ek'),
                                    'ed':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ed'),
                                    'ek':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ek'),
                                    'Benef Name': v.get('OPERINFO').get('OPER').get('NAMEKORR'),
                                    'Benef Account' : v.get('OPERINFO').get('OPER').get('ACCKORR'),
                                    'Benef Bic' : v.get('OPERINFO').get('OPER').get('MFOKORR'),
                                    'Ground' : v.get('OPERINFO').get('OPER').get('DETPAY'),
                                    'UNPKORR' : v.get('OPERINFO').get('OPER').get('UNPKORR'),
                                    }
            except AttributeError:
                isinstance(v.get('OPERINFO').get('OPER'), list)
                data['i'] = i
                data['AccountNumber']=v.get('ACCOUNT')
                data['CurrCode']=v.get('CURRENCY').get('@Code')
                data['Currency'] = v.get('CURRENCY').get('@Iso')
                data['DocumentDate'] = date_issue(v.get('PERIOD')[3:])
                for index, doc in enumerate(v.get('OPERINFO').get('OPER'), 1):
                    data[index] = {
                                            'doc':doc.get('DOCN'),
                                            'nd':doc.get('SUMOPER').get('@nd'),
                                            'nk':doc.get('SUMOPER').get('@ek'),
                                            'ed':doc.get('SUMOPER').get('@ed'),
                                            'ek':doc.get('SUMOPER').get('@ek'),
                                            'Benef Name': doc.get('NAMEKORR'),
                                            'Benef Account' : doc.get('ACCKORR'),
                                            'Benef Bic' : doc.get('MFOKORR'),
                                            'Ground' : doc.get('DETPAY'),
                                            'UNPKORR' : doc.get('UNPKORR'),
                                        }
        except:
            error = f'\n {index}, \n {doc},\n{v}'
            with open('error.txt', 'w') as f:
                f.write(error)     
        data_list.append(data)
    return data_list



def solve_issue(index, v, data):
    data[index] = {
                    'doc':v.get('OPERINFO').get('OPER').get('DOCN'),
                    'nd':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@nd'),
                    'nk':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ek'),
                    'ed':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ed'),
                    'ek':v.get('OPERINFO').get('OPER').get('SUMOPER').get('@ek'),
                    'Benef Name': v.get('OPERINFO').get('OPER').get('NAMEKORR'),
                    'Benef Account' : v.get('OPERINFO').get('OPER').get('ACCKORR'),
                    'Benef Bic' : v.get('OPERINFO').get('OPER').get('MFOKORR'),
                    'Ground' : v.get('OPERINFO').get('OPER').get('DETPAY'),
                    'UNPKORR' : v.get('OPERINFO').get('OPER').get('UNPKORR'),
                }
    return data


def get_id(data_list):
    '''Считаем количество строк documents сколько последнего id, в переменную док отправляем документ, если дебетовый счет, то по дебету, по кредите, то по кредиту. '''
    number = list(data_list.items())
    try:
        number_of_doc = int(number[-1][0])
        doc = ''
        doc_dbt = ''
        doc_crt = ''
        data = data_list
        for i in range(1, number_of_doc + 1):
            if data[i].get('nk') == '':
                debet_doc = f'''\t\t\t<Document>
                <DocumentNumber>{data[i].get('doc')}</DocumentNumber> 
                <DocumentDate>{data['DocumentDate']}</DocumentDate>
                <Amount>{data[i].get('ed')}</Amount>
                <Beneficiar>
                    <Name>{data[i].get('Benef Name')}</Name>
                    <UNP>{data[i].get('UNPKORR')}</UNP>
                    <Account>{data[i].get('Benef Account')}</Account>
                    <BIC>{data[i].get('Benef Bic')}</BIC>
                </Beneficiar>
                <Ground>{data[i].get('Ground')}</Ground>
            </Document>
'''
                doc_dbt += debet_doc
            elif data[i].get('nd') == '':
                credit_doc = f'''\t\t\t<Document>
                <DocumentNumber>{data[i].get('doc')}</DocumentNumber> 
                <DocumentDate>{data['DocumentDate']}</DocumentDate>
                <Amount>{data[i].get('ek')}</Amount>
                <Payer>
                    <Name>{data[i].get('Benef Name')}</Name>
                    <UNP>{data[i].get('UNPKORR')}</UNP>
                    <Account>{data[i].get('Benef Account')}</Account>
                    <BIC>{data[i].get('Benef Bic')}</BIC>
                </Payer>
                <Ground>{data[i].get('Ground')}</Ground>
            </Document>
'''
                doc_crt += credit_doc
                #import pdb;pdb.set_trace()
            doc = f'<DebetDocuments>\n{doc_dbt}\t\t\t</DebetDocuments>\n\t\t<CreditDocuments>\n {doc_crt}\t\t\t</CreditDocuments>'
        return doc
        
    except:
        with open('error.txt', 'a+') as f:
            f.write('\n')
            f.write(str(number))
            f.write(str(data_list))

def to_xml(data, path):
    '''Приводим к нужный вид данные из дикта'''
    data = [i for i in data if i]
    doc = ''
    for e, a in enumerate(data,1):
        try:
            document = f"""<Statement>
        <AccountNumber>{a['AccountNumber']}</AccountNumber>
        <CurrCode>{a['CurrCode']}</CurrCode>
        <CurrCodeISO>{a['Currency']}</CurrCodeISO>{get_id(a)}
\t</Statement>\n\t"""
        except KeyError:
            #import pdb;pdb.set_trace()
            print(e)
            document = f"""<Statement>
        <AccountNumber>{a['AccountNumber']}</AccountNumber>
        <CurrCode>{a['CurrCode']}</CurrCode>
        <CurrCodeISO>{a['Currency']}</CurrCodeISO>
       \t</Statement>\n\t"""
            error(a)
        doc += document
    doc = f'<Statements>\n\t{doc}\n\t</Statements>'
    return doc



def error(i):
    with open('error.txt', 'a+') as f:

        f.write('\n')
        f.write(str(i))


def save_xml(document, name, path):
    with open(f'{path[:48]}{name}_.xml', 'w', encoding = 'utf-8') as f:
            f.write(document)


def month_base(file):
    with open(file, 'r', encoding='UTF-8') as f:
        xml = f.read()
        xml = xml.replace('</TURN><?xml version="1.0" encoding="cp866"?>\n<TURN>','')
        info = xmltodict.parse(str(xml))
        turn = info.get('TURN')
        acc = turn.get('ACCOUNTINFO')
        return acc


def main(path:str):
    name = path[48:56]
    month = month_base(path)
    collect = collect_data(month)
    result = to_xml(collect,path)
    save_xml(result, name,path)




main('/media/sun/SUN/SunPharma/Выписки XML/2019/2/byn/01022019.xml_prsd.xml')
main('/media/sun/SUN/SunPharma/Выписки XML/2019/2/usd/01022019.xml_prsd.xml')

main('/media/sun/SUN/SunPharma/Выписки XML/2019/3/byn/01032019.xml_prsd.xml')
main('/media/sun/SUN/SunPharma/Выписки XML/2019/3/usd/01032019.xml_prsd.xml')

main('/media/sun/SUN/SunPharma/Выписки XML/2019/4/byn/01042019.xml_prsd.xml')
main('/media/sun/SUN/SunPharma/Выписки XML/2019/4/usd/01042019.xml_prsd.xml')

main('/media/sun/SUN/SunPharma/Выписки XML/2019/5/byn/01052019.xml_prsd.xml')
main('/media/sun/SUN/SunPharma/Выписки XML/2019/5/usd/01052019.xml_prsd.xml')

main('/media/sun/SUN/SunPharma/Выписки XML/2019/6/byn/01062019.xml_prsd.xml')
main('/media/sun/SUN/SunPharma/Выписки XML/2019/6/usd/01062019.xml_prsd.xml')