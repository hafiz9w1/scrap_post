{
    'name': 'Inventory Scrap Notification',
    'version': '15.0.1.0.1',
    'category': 'Inventory/Purchase',
    'summary': """
        Inventory Scrap Notification
        """,

    'description': """
        Notification of Accounts department group after
        scrapping of a product is done with an accounting entry
    """,

    'author': 'Hafiz Abbas',
    'email': 'hafizabbas9w1@gmail.com',
    'depends': ['stock', 'sale', 'project', 'purchase', 'product'],

    'data': [
        'views/stock_scrap.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
