# -*3- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
import re
from odoo import exceptions

class StockMoveLine(models.Model):
    #_name = "account.aged.partner.inherit"
    _inherit = 'stock.move.line'


    codigo_id = fields.Many2one('res.users', string='Codigo',)
    number = fields.Char(string='Numero',related='picking_id.origin')
    customer_id = fields.Many2one('res.partner', string='Cliente o Proveedor',related='picking_id.partner_id')
    entrada = fields.Float(string='Entrada',compute='_compute_entrada')
    salida = fields.Float(string='Salida',compute='_compute_salida')
    saldo_existencia = fields.Float(string='Saldo en existencia', compute='saldo_existencias')
    
    @api.depends('qty_done','reference')
    def _compute_entrada(self):        
        for record in self:
            #   Cantidad de producto actualizada
            if record.location_id.id == 14 and record.location_id.name == 'Inventory adjustment':
                record.entrada = record.qty_done

            # Recibo
            elif record.picking_code == "incoming":
                record.entrada = record.qty_done

            #Transferencia Interna
            elif record.picking_code == "internal":
                record.entrada = record.qty_done

            #Fabricacion
            elif record.picking_code == "mrp_operation":
                record.entrada = record.qty_done
            else:
                record.entrada = 0.0

    @api.depends('qty_done','reference')
    def _compute_salida(self):
        for record in self:
            #   Cantidad de producto actualizada
            if record.picking_code == False and record.location_dest_id.name == 'Inventory adjustment':
                record.salida = record.qty_done

            #Transferencia Interna
            elif record.picking_code == "internal":
                record.salida = record.qty_done

            #Envio
            elif record.picking_code == "outgoing":
                record.salida = record.qty_done

            else:
                record.salida = 0.0

    # @api.depends('entrada','salida')
    # def _compute_saldo_existencia(self):
    #     anterior =0.0



    #     for record in self:
    #         #record.saldo_existencia = record.salida + record.entrada
    #         existencia = record.product_id.qty_available - record.qty_done

    #         if existencia == 0:
    #             record.saldo_existencia = record.qty_done
    #         elif record.location_id.id == 14 and record.location_id.name == 'Inventory adjustment':
    #             record.saldo_existencia = record.qty_done + anterior 
    #         elif record.picking_code == False and record.location_dest_id.name == 'Inventory adjustment':
    #             record.saldo_existencia = anterior - record.qty_done
    #         elif record.picking_code == "internal":
    #             record.saldo_existencia = anterior
    #         elif record.picking_code == "outgoing":
    #             record.saldo_existencia = anterior - record.qty_done
    #         else:
    #             record.saldo_existencia = record.qty_done + anterior            
    #         anterior = record.saldo_existencia

    # records = self.env['stock.move.line'].search([])
    # records.mapped(lambda self: self.saldo_existencia())

    
    def saldo_existencias(self):
            
        for record in self:

            if record.state == 'done':
                quants = self.env['stock.quant'].search([('product_id','=',record.product_id.id),('in_date','<=',record.date),('inventory_date','=',False)],order="id asc")
                available_quantity = sum(quants.mapped('reserved_quantity'))- sum(quants.mapped('quantity'))
                #import pdb; pdb.set_trace()
                # if len(quants) == 0:
                #     record.saldo_existencia = record.qty_done
                # if len(quants) == 1:
                #     record.saldo_existencia = record.qty_done

                # elif len(quants) > 1:
                #     saldo_existe = 0.00
                #     saldo_existe1 = 0.00
                #     saldo_existe2 = 0.00
                #     saldo_existe3 = 0.00
                    
                    # for q in quants:
                    #     available_quantity = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
                

                    #     if q.quantity and record.location_id.usage == 'inventory' and record.location_dest_id.usage == 'internal':
                    #         saldo_existe1 += q.quantity
                    #         #record.saldo_existencia = saldo_existe
                    #         #record.saldo_existencia = saldo_existe - record.qty_done
                    #     elif q.quantity and record.location_id.usage == 'supplier' and record.location_dest_id.usage == 'internal':
                    #         saldo_existe2 += record.qty_done
                    #         #record.saldo_existencia = saldo_existe 
                    #     elif q.quantity and record.location_id.usage == 'internal' and record.location_dest_id.name == 'Customers':
                    #         saldo_existe3 += record.qty_done
                    #         #record.saldo_existencia = saldo_existe - record.qty_done
                    #     else:
                    #         record.saldo_existencia = record.qty_done
                    #saldo = saldo_existe1 + saldo_existe2 - saldo_existe3
                record.saldo_existencia = available_quantity
            else:
                quants_disp = self.env['stock.quant'].search([('product_id','=',record.product_id.id),('in_date','<',record.date),('inventory_date','=',False)],order="id asc")
                available_quantity_dispo = sum(quants_disp.mapped('reserved_quantity'))- sum(quants_disp.mapped('quantity'))
         
                record.saldo_existencia = available_quantity_dispo
                    
            #     else:
            #         record.saldo_existencia = record.qty_done
            # else:
            #         record.saldo_existencia = record.qty_done



            # elif record.picking_code == "internal":
            #     record.saldo_existencia = saldo_existe
            # elif record.picking_code == "outgoing":
            #     record.saldo_existencia = saldo_existe - record.qty_done
            # elif record.picking_code == "incoming":
            #     record.saldo_existencia = saldo_existe - record.qty_done
            # else:
            #     if record.location_id.usage == 'inventory' and record.location_dest_id.usage == 'internal':
            #         record.saldo_existencia = record.qty_done + saldo_existe
            #         #record.saldo_existencia = saldo_existe - record.qty_done
            #     if record.location_id.usage == 'supplier' and record.location_dest_id.usage == 'internal':
            #         record.saldo_existencia = saldo_existe + record.qty_done 
            #     if record.location_id.usage == 'internal' and record.location_dest_id.name == 'Customers':
            #          record.saldo_existencia = saldo_existe - record.qty_done
            

            # x = record.product_id.qty_available
            # if x == record.qty_done:
            #     record.saldo_existencia = x
            # #indice = record.index(self)
            # #if record[0] in self:
            #     #record.saldo_existencia = x
            # else:
            #     indice = record.index(self)
            #     position = indice - 1
            #     record.saldo_existencia = self[position].product_id.qty_available - self[position].product_id.qty_done


    # def _compute_quantities(self):
    #     products = self.filtered(lambda p: p.type != 'service')
    #     res = products._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
    #     for product in products:
    #         product.qty_available = res[product.id]['qty_available']
    #         product.incoming_qty = res[product.id]['incoming_qty']
    #         product.outgoing_qty = res[product.id]['outgoing_qty']
    #         product.virtual_available = res[product.id]['virtual_available']
    #         product.free_qty = res[product.id]['free_qty']
    #     # Services need to be set with 0.0 for all quantities
    #     services = self - products
    #     services.qty_available = 0.0
    #     services.incoming_qty = 0.0
    #     services.outgoing_qty = 0.0
    #     services.virtual_available = 0.0
    #     services.free_qty = 0.0

    # def _compute_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
    #     domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
    #     domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
    #     dates_in_the_past = False
    #     # only to_date as to_date will correspond to qty_available
    #     to_date = fields.Datetime.to_datetime(to_date)
    #     if to_date and to_date < fields.Datetime.now():
    #         dates_in_the_past = True

    #     domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
    #     domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
    #     if lot_id is not None:
    #         domain_quant += [('lot_id', '=', lot_id)]
    #     if owner_id is not None:
    #         domain_quant += [('owner_id', '=', owner_id)]
    #         domain_move_in += [('restrict_partner_id', '=', owner_id)]
    #         domain_move_out += [('restrict_partner_id', '=', owner_id)]
    #     if package_id is not None:
    #         domain_quant += [('package_id', '=', package_id)]
    #     if dates_in_the_past:
    #         domain_move_in_done = list(domain_move_in)
    #         domain_move_out_done = list(domain_move_out)
    #     if from_date:
    #         date_date_expected_domain_from = [('date', '>=', from_date)]
    #         domain_move_in += date_date_expected_domain_from
    #         domain_move_out += date_date_expected_domain_from
    #     if to_date:
    #         date_date_expected_domain_to = [('date', '<=', to_date)]
    #         domain_move_in += date_date_expected_domain_to
    #         domain_move_out += date_date_expected_domain_to

    #     Move = self.env['stock.move'].with_context(active_test=False)
    #     Quant = self.env['stock.quant'].with_context(active_test=False)
    #     domain_move_in_todo = [('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
    #     domain_move_out_todo = [('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
    #     moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
    #     moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
    #     quants_res = dict((item['product_id'][0], (item['quantity'], item['reserved_quantity'])) for item in Quant.read_group(domain_quant, ['product_id', 'quantity', 'reserved_quantity'], ['product_id'], orderby='id'))
    #     if dates_in_the_past:
    #         # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
    #         domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
    #         domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
    #         moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
    #         moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))

    #     res = dict()
    #     for product in self.with_context(prefetch_fields=False):
    #         origin_product_id = product._origin.id
    #         product_id = product.id
    #         if not origin_product_id:
    #             res[product_id] = dict.fromkeys(
    #                 ['qty_available', 'free_qty', 'incoming_qty', 'outgoing_qty', 'virtual_available'],
    #                 0.0,
    #             )
    #             continue
    #         rounding = product.uom_id.rounding
    #         res[product_id] = {}
    #         if dates_in_the_past:
    #             qty_available = quants_res.get(origin_product_id, [0.0])[0] - moves_in_res_past.get(origin_product_id, 0.0) + moves_out_res_past.get(origin_product_id, 0.0)
    #         else:
    #             qty_available = quants_res.get(origin_product_id, [0.0])[0]
    #         reserved_quantity = quants_res.get(origin_product_id, [False, 0.0])[1]
    #         res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
    #         res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
    #         res[product_id]['incoming_qty'] = float_round(moves_in_res.get(origin_product_id, 0.0), precision_rounding=rounding)
    #         res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(origin_product_id, 0.0), precision_rounding=rounding)
    #         res[product_id]['virtual_available'] = float_round(
    #             qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],
    #             precision_rounding=rounding)

    #       return res