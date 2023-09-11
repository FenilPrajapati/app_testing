{
    'name': 'FreightBox Base',
    'category': 'Freight',
    'description': """
    """,
    'author': 'PowerpBox IT Solutions Pvt Ltd',
    'depends': ['base', 'web', 'crm', 'sale', 'sale_crm', 'sale_management', 'purchase',
                'account', 'website', 'mail', 'stock','portal', 'maintenance','hr'],
    'website': 'https://www.powerpbox.org/',
    'version': '1.0',
    'license': 'OPL-1',
    'images': [
        
        'static/description/banner.gif',
        'static/src/img/correct.png',
        
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'data/charges_data.xml',
        'data/charges_template_data.xml',
        # 'data/ports_template_data.xml',
        
        'data/port_data.xml',
        
        'data/facility_type_code_data.xml',
       
       
        'data/shipping_containers_data.xml',
        'data/container.iso.code.csv',
       
        'views/port_view.xml',
        
        'views/container_iso_code_view.xml',
        'views/facility_type_view.xml',
        
        'views/charges_view.xml',
        'views/mrg_charges_view.xml',
        
        'views/menu_view.xml',
        # 'data/mail_template_data.xml',


        
        
    ],
    'assets': {
        # 'web.assets_backend': [
            
        #     'freightbox_contracts/static/src/scss/contract_dashboard.scss',
            
        #     'freightbox_contracts/static/src/js/contract_dashboard.js',
            
        #     "freightbox_contracts/static/src/xml/contract_dashboard.xml",
            
        # ],
        
    },
    'installation': True
}
