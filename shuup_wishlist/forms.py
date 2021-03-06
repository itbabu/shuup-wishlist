# -*- coding: utf-8 -*-
# This file is part of Shuup Wishlist.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms

from shuup.core.models import Product
from shuup_wishlist.models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['name', 'privacy']

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        self.customer = kwargs.pop('customer', None)
        self.product_id = kwargs.pop('product_id', None)
        super(WishlistForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if self.product_id:
            product = Product.objects.get(pk=self.product_id)
            shop_product = product.get_shop_instance(self.shop)
            errors = shop_product.get_visibility_errors(self.customer)
            for error in errors:
                self.add_error(None, error)
        return super(WishlistForm, self).is_valid()
