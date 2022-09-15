# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
#import requests


class StockQuantReposition(models.TransientModel):
    _name = 'stock.quant.reposition'
    _description = 'Reposicion de Inventario'

    #Deposito
    product_id = fields.Many2one('product.product', string='Producto',)
    producto = fields.Char(string='Producto C',)
        #domain=lambda self: self._domain_product_id(),
        #ondelete='restrict', required=True, index=True, check_company=True)
    #product_tmpl_id = fields.Many2one(
    #    'product.template', string='Product Template',
    #    related='product_id.product_tmpl_id')
    deposito_principal_mgta = fields.Float(string='DEP 01 MGTA',)
    deposito_principal_ccs = fields.Float(string='INV CCS',)
    deposito_principal_bto = fields.Float(string='INV BQTO',)
    deposito_principal_val = fields.Float(string='INV VAL',)
    #Ventas
    ventas_fta_mgta = fields.Float(string='FACT MGTA',)
    ventas_ne_mgta = fields.Float(string='NE MGTA',)
    ventas_real_mgta = fields.Float(string='VENTAS MGTA (REAL)',)
    ventas_fta_ccs = fields.Float(string='FACT CCS',)
    ventas_ne_ccs = fields.Float(string='NE CCS',)
    ventas_real_ccs = fields.Float(string='VENTAS CCS (REAL)',) 
    ventas_fta_bto = fields.Float(string='FACT BTO',)
    ventas_ne_bto = fields.Float(string='NE BTO',)
    ventas_real_bto = fields.Float(string='VENTAS BTO (REAL)',)
    ventas_fta_val = fields.Float(string='FACT VAL',)
    ventas_ne_val = fields.Float(string='NE VAL',)
    ventas_real_val = fields.Float(string='VENTAS VAL (REAL)',)
    #Stock
    stock_mgta = fields.Float(string='STOCK MGTA',)
    stock_ccs = fields.Float(string='STOCK CCS',)
    stock_bto = fields.Float(string='STOCK BQTO',)
    stock_val = fields.Float(string='STOCK VAL',)
    stock_tierra_firme = fields.Float(string='STOCK TIERRA FIRME',)
    #Alertas
    alerta_reposicion_mgta = fields.Boolean(string='Reposición MGTA?',)
    alerta_reposicion_bto = fields.Boolean(string='Reposición BTO?',)
    alerta_reposicion_val = fields.Boolean(string='Reposición VAL?',)
    alerta_pedido_proveedor = fields.Boolean(string='Pedido a Proveedor? ',)
    #Minimos
    minimo_global = fields.Integer(string='Minimo Global',)
    minimo_sede = fields.Integer(string='Minimo Sede',)   



    # def _domain_product_id(self):
    #     if not self._is_inventory_mode():
    #         return
    #     domain = [('type', '=', 'product')]
    #     if self.env.context.get('product_tmpl_ids') or self.env.context.get('product_tmpl_id'):
    #         products = self.env.context.get('product_tmpl_ids', []) + [self.env.context.get('product_tmpl_id', 0)]
    #         domain = expression.AND([domain, [('product_tmpl_id', 'in', products)]])
    #     return domain


    # @api.model
    # def _is_inventory_mode(self):
    #     """ Used to control whether a quant was written on or created during an
    #     "inventory session", meaning a mode where we need to create the stock.move
    #     record necessary to be consistent with the `inventory_quantity` field.
    #     """
    #     return self.env.context.get('inventory_mode') and self.user_has_groups('stock.group_stock_user')


    def js_python_method(self, model_name, active_id):
        reposition_form = self.env.ref('stock_move_line_report_rep.stock_inventory_reposition_form_view', False)
        return {
            'name': 'Inventario a partir de:',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inventory.reposition',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'views': [(reposition_form.id, 'form')],
            'view_id': reposition_form.id,
            'flags': {'action_buttons': True},
        }


        #report_obj = self.env['ir.actions.act_window']
        #return report_obj.('stock_move_line_report_rep.stock_inventory_reposition_form_view')
        #return report_obj.render('stock_move_line_report_rep.stock_inventory_reposition_form_view')
        #return requests.render('stock_inventory_reposition_form_view') 
        #render(self, stock_inventory_reposition_form_view)
        #print("Hello from a function")
        # ret_list = []
        # req = (
        #            "SELECT sale_order.name, rp.name AS customer, sale_order.amount_total, sale_order.state "
        #            "FROM sale_order "
        #            "Join res_partner rp ON (sale_order.partner_id=rp.id)")
        # self.env.cr.execute(req)
        # for rec in self.env.cr.dictfetchall():
        #     ret_list.append(rec)
        # return ret_list     
        """ Method called from JS custom button ""
        .... your python logic here! .....   """