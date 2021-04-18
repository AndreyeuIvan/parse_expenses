'''I will try to use xml_to_dict because, I get errors, witch I can not pass. Eqrlier librarie is sucks.'''

''' 1. Take file.
    2. Count tags
    3. Take needfull tags
    4. Get objects
    5. Transform objects into new form.'''

import xmltodict
from datetime import datetime


def date_issue(date):
    '''Change date into propriet format'''
    date = date.replace('.','-')
    date = datetime.strptime(date, '%d-%m-%Y')
    date = date.isoformat()[:10]
    return date


def collect_data(file):
    '''здесь мы обрабатываем запрос, выделяем объекты и складывем в дикт.'''
    data_list = []
    for i, v in enumerate(file,1):
        data = {}
        data['i'] = i
        data['AccountNumber']=v.get('ACCOUNT')
        data['CurrCode']=v.get('CURRENCY').get('@Code')
        data['Currency'] = v.get('CURRENCY').get('@Iso')
        data['DocumentDate'] = date_issue(v.get('PERIOD')[3:])
        for index, doc in enumerate(v.get('OPERINFO').get('OPER'), 1):
            if doc == 'OPERUID':
                solve_issue(index, v, data)
            try:
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
                error = f'\n {index}, \n {doc}'
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


def to_xml(data):
    '''Приводим к нужный вид данные из дикта'''
    doc = ''
    for i in data:
        try:
            document = f"""<Statement>
        <AccountNumber>{i['AccountNumber']}</AccountNumber>
        <CurrCode>{i['CurrCode']}</CurrCode>
        <CurrCodeISO>{i['Currency']}</CurrCodeISO>
        {get_id(i)}
    \t</Statement>\n\t"""
        except:
            import pdb;pdb.set_trace()
            document = f"""<Statement>
        <AccountNumber>{i['AccountNumber']}</AccountNumber>
        <CurrCode>{i['CurrCode']}</CurrCode>
        <CurrCodeISO>{i['Currency']}</CurrCodeISO>
        {solve_issue(i)}
    \t</Statement>\n\t"""
            error(i)
        doc += document
    doc = f'<Statements>\n\t{doc}\n\t</Statements>'
    return doc


def error(i):
    with open('error.txt', 'a+') as f:
        f.write('\n')
        f.write(str(i))


def save_xml(document):
    with open('res1.xml', 'w', encoding = 'utf-8') as f:
            f.write(document)


def month_base(file):
    with open(file, 'r', encoding='UTF-8') as f:
        xml = f.read()
        info = xmltodict.parse(str(xml))
        turn = info.get('TURN')
        acc = turn.get('ACCOUNTINFO')
        return acc


month = month_base('/home/sun/Desktop/python/work/work/new_programm/20190603-20190830_бин_2_не получится.xml')
collect = collect_data(month)
result = to_xml(collect)
save_xml(result)