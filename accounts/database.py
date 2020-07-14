def partner_resume(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/resume'+'.'+ext).format(instance.pk)


def partner_photo(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/photo'+'.'+ext).format(instance.partner.pk)


def partner_ec(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/ec'+'.'+ext).format(instance.partner.pk)


def partner_aadhar(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/aadhar'+'.'+ext).format(instance.partner.pk)


def partner_pan(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/pan'+'.'+ext).format(instance.partner.pk)


def partner_worexp(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/worexp'+'.'+ext).format(instance.partner.pk)


def partner_ps(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/partner/{0}/ps'+'.'+ext).format(instance.partner.pk)


def order(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/order/{0}/document'+'.'+ext).format(instance.pk)


def client_logo(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/logo'+'.'+ext).format(instance.client.pk)


def client_pan(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/pan'+'.'+ext).format(instance.client.pk)


def client_tan(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/tan'+'.'+ext).format(instance.client.pk)


def client_photo(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/photo'+'.'+ext).format(instance.client.pk)


def client_aadhar(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/aadhar'+'.'+ext).format(instance.client.pk)


def client_cpan(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/cpan'+'.'+ext).format(instance.client.pk)


def client_coinc(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/coinc'+'.'+ext).format(instance.client.pk)


def client_ps(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/client/{0}/ps'+'.'+ext).format(instance.client.pk)


def product(instance, filename):
    ext = filename.split('.')[-1]
    return ('media/product/{0}/document'+'.'+ext).format(instance.pk)


NAME = 'fs1'
USER = 'root'
PASSWORD = "san@2912"
HOST = ""
PORT = ""

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
TYPE_OF_COMPANY =[('select','select'),('Private Limited', 'Private Limited'), ('Proprietorship Firm', 'Proprietorship Firm'), ('LLP', 'LLP'), ('Individual', 'Individual'), ('Society', 'Society'), ('Others', 'Others')]
AUTHORIZED_PERSON_POSITION = [('select','select'),('Director', 'Director'), ('Financial Manager', 'Financial Manager'), ('Partner', 'Partner'), ('Managing Partner', 'Managing Partner'), ('Employe', 'Employe'), ('Head of Finance', 'Head of Finance'), ('Others', 'Others')]