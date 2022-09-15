# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
import datetime
import pdb


class StockInventoryReposition(models.TransientModel):
    _name = 'stock.inventory.reposition'
    _description = 'Inventory Reposition'

    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     if self.env.context.get('default_quant_ids'):
    #         quants = self.env['stock.quant'].browse(self.env.context['default_quant_ids'])
    #         res['show_info'] = any(not quant.inventory_quantity_set for quant in quants)
    #     return res

    #def _default_inventory_adjustment_name(self):
        #return _("Reposicion de Inventaro") + " - " + fields.Date.to_string(fields.Date.today())

    #quant_ids = fields.Many2many('stock.quant')
    #inventory_adjustment_name = fields.Char(default=_default_inventory_adjustment_name)
    show_info = fields.Boolean('Show warning')
    desde_fecha = fields.Datetime(string='Desde', default=lambda self: fields.Date.today())
    hasta_fecha = fields.Datetime(string='Hasta', compute='_compute_hasta_fecha')

    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @api.depends('desde_fecha')
    def _compute_hasta_fecha(self):
        self.hasta_fecha = self.desde_fecha + datetime.timedelta(days=15)
    
    def action_apply(self):

        # Logica para obtener la consulta de reposicion de inventario desde la fecha seleccionada hasta 15 dias despues de la seleccionada
        compania = self.env.user.company_id
        quants = self.env['stock.quant'].search([('company_id','=',compania.id)])
        reposiciones = self.env['stock.quant.reposition'].search([])
        products = self.env['product.product'].search([('detailed_type','=','product')])
            
        if quants and reposiciones and products:
            repo = self.env['stock.quant.reposition'].search([]).sudo().unlink()
            quant_ccs = 0.0
            quant_mgt = 0.0
            quant_bto = 0.0
            quant_val = 0.0            

            for product in products:
                product_id = product.id
                quant_product = self.env['stock.quant'].search([('product_id','=',product_id),('in_date','>=',self.desde_fecha),('in_date','<=',self.hasta_fecha)])
                name_categoria = product.categ_id.name + ' ' + product.name
                
                #recorro los quants de cada producto
                for qproduct in quant_product:
                    #Rama Caracas WHCCS
                    if qproduct.location_id.warehouse_id.branch_id.id == 1 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_ccs = qproduct.quantity
                    #Rama Barquisimeto WHBTO
                    if qproduct.location_id.warehouse_id.branch_id.id == 2 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_bto = qproduct.quantity
                    #Rama Margarita WHMgt
                    if qproduct.location_id.warehouse_id.branch_id.id == 3 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_mgt = qproduct.quantity
                    #Rama Valencia WHVAL
                    if qproduct.location_id.warehouse_id.branch_id.id == 4 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_val = qproduct.quantity
                    #for reposicion in reposiciones:
                    #    write = reposicion.write({'product_id' : product_id, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt, 'deposito_principal_ccs': quant_ccs, 'deposito_principal_bto': quant_bto, 'deposito_principal_val': quant_val})
                new = reposiciones.create({'product_id' : product_id, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt, 'deposito_principal_ccs': quant_ccs, 'deposito_principal_bto': quant_bto, 'deposito_principal_val': quant_val})

        elif quants and products:
            #Recorro los productos
            reposiciones = self.env['stock.quant.reposition']
            quant_ccs = 0.0
            quant_mgt = 0.0
            quant_bto = 0.0
            quant_val = 0.0
            for product in products:
                product_id = product.id
                quant_product = self.env['stock.quant'].search([('product_id','=',product_id),('in_date','>=',self.desde_fecha),('in_date','<=',self.hasta_fecha)])
                #recorro los quants de cada producto
                name_categoria = product.categ_id.name + ' ' + product.name
                
                for qproduct in quant_product:
                    # is_main = qproduct.location_id.
                    # if is_main == True:
                    #Rama Caracas WHCCS
                    if qproduct.location_id.warehouse_id.branch_id.id == 1 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_ccs = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_ccs': quant_ccs})
                    #Rama Barquisimeto WHBTO
                    if qproduct.location_id.warehouse_id.branch_id.id == 2 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_bto = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_bto': quant_bto})
                    #Rama Margarita WHMgt
                    if qproduct.location_id.warehouse_id.branch_id.id == 3 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_mgt = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt})
                    #Rama Valencia WHVAL
                    if qproduct.location_id.warehouse_id.branch_id.id == 4 and qproduct.location_id.warehouse_id.is_main == True:
                        quant_val = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_val': quant_val})
                new = reposiciones.create({'product_id' : product_id, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt, 'deposito_principal_ccs': quant_ccs, 'deposito_principal_bto': quant_bto, 'deposito_principal_val': quant_val})


        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }