import requests
from lxml import html


def ConnectHelper(login, password):
    response = requests.get('http://entrecles.eedf.fr/Default.aspx', headers={"Connection":"close"})
    tree = html.fromstring(response.text)
    params = {
        '__VIEWSTATE': tree.get_element_by_id('__VIEWSTATE').value,
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': tree.get_element_by_id('__EVENTVALIDATION').value,
        'ctl00$MainContent$login': login,
        'ctl00$MainContent$password': password,
        'ctl00$MainContent$_btnValider': 'Se connecter',
    }
    response = requests.post(
        'http://entrecles.eedf.fr/Default.aspx',
        data=params,
        headers={"Connection":"close"}
    )
    name = 'unknown'
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        try:
            div = tree.get_element_by_id('ctl00__divLogin')
            name = div.text
        except:
            print("Fail to authenticate")

    response.connection.close()
    return name