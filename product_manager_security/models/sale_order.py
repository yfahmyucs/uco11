# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if 'order_line' not in vals:
            raise UserError("Please add lines in Quotation")
        res = super(SaleOrder, self.sudo()).create(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self.sudo()).write(vals)
        return res



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self.sudo()).create(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self.sudo()).write(vals)
        return res

    @api.depends("product_id")
    def _get_prodcut_managers(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.categ_id.managers_id:
                    rec.managers_id = rec.product_id.categ_id.managers_id

    managers_id = fields.Many2many('res.users', compute="_get_prodcut_managers", string='Product Managers', store=True)

    state_confirm = fields.Selection([
        ('confirm', 'Confirm')], store=True)

    @api.multi
    @api.onchange('state_confirm')
    def _check_manager(self):
        for line in self:
            if line.product_id:
                if self.env.user.has_group('base.group_system'):
                    pass
                elif line.managers_id:
                    if self.env.user.id not in line.managers_id.ids:
                        raise ValidationError("PM Should Confirm")


