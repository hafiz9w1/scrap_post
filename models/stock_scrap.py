from odoo import models, fields, _


class stock_scrap(models.Model):
    _inherit = 'stock.scrap'

    scrap_reason = fields.Selection(
        [
            ('damaged_goods', 'Impaired / Damaged Goods'),
            ('design_changes', 'Impaired / Design Changes'),
        ],
        string='Reason for Scrapping',
        required=True,
    )

    def do_scrap(self):
        """
        Send notification to Accounts department group after
        scrapping is validated
        """
        res = super(stock_scrap, self).do_scrap()
        account_users = self.env.ref('account.group_account_manager').users
        scrap_reasons = dict(self._fields['scrap_reason'].selection)
        for scrap in self:
            scrap_unit_cost = scrap.move_id.stock_valuation_layer_ids.unit_cost
            if scrap.move_id.account_move_ids:
                msg = _(
                    '<br>Subject: Scrapping Posting Review<br><br>'
                    'A Journal Entry was created from Scrapping.<br><br>'
                    'Scrap Order No: {scrap_name}<br>'
                    'Product: {product_name}<br>'
                    'Quantity: {product_quantity}<br>'
                    'Price: {product_price}<br>'
                    'Total Value: {product_value}<br>'
                    'Reason: {scrap_reason}<br>'
                    'Responsible User: {scrap_responsible_user}<br><br>'
                    'Best regards <br>'
                    'Inventory Department <br>'
                    .format(scrap_name=scrap.name,
                            product_name=scrap.product_id.product_tmpl_id.display_name,
                            product_quantity=scrap.scrap_qty,
                            product_price=scrap_unit_cost,
                            product_value=scrap.scrap_qty * scrap_unit_cost,
                            scrap_reason=scrap_reasons.get(scrap.scrap_reason),
                            scrap_responsible_user=scrap.env.user.partner_id.name),
                )
                scrap.message_post(
                    body=msg,
                    subject='Scraping Posting Review',
                    message_type='email',
                    subtype_xmlid='mail.mt_comment',
                    notification_ids=[(0, 0, {
                        'res_partner_id': user.partner_id.id,
                        'notification_type': 'email'},
                    ) for user in account_users],
                )
        return res

    def action_open_scrap_account_move(self):
        """
        Get account entries generated from scrapping
        """
        action = self.env['ir.actions.act_window']._for_xml_id(
            'account.action_move_journal_line')
        action['domain'] = [('stock_move_id', '=', self.move_id.id)]
        return action
