************************
Hibou - Partner Gravatar
************************

Provides an easy way to get partner images from the Gravatar service. For more information and add-ons, visit `Hibou.io <https://hibou.io/>`_.


=============
Main Features
=============
* Download images on email change
* Ability to upload your own images (bypass Gravatar)
* Maintain stock images if no email is provided
* Configure different icon sets for companies vs individuals

=====
Usage
=====

Whenever you create a new partner, or change a partner's email address, the Gravatar service will be used to update the image.
You can 'delete' the image at any time to also update the image (otherwise it is saved or updated only on change).


Customization
=============

Upon first use, two `ir.config_parameter` keys will be created with the default values of *identicon*.

* `gravatar.icon_set`
* `gravatar.icon_set.company`

The values of these keys can be any of the usual Gravatar icon sets. See `Gravatar API <https://en.gravatar.com/site/implement/images/>`_.

Currently this means:

* `404` (don't use this one)
* `mm` (practically useless)
* `identicon`
* `monsterid`
* `wavatar`
* `retro`
* `blank` (boring)

To edit these values, you need to activate the Developer/Debug menu by choosing `About` from the top right menu bar, and hitting the `Activate the developer mode` button.
Next navigate to `Settings->Technical->Parameters->System Parameters` and search for `gravatar`.

=======
Licence
=======

Please see `LICENSE <https://github.com/hibou-io/website-project/blob/master/LICENSE>`_.

Copyright Hibou Corp. 2016.
