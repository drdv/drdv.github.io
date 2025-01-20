# My public GPG key

[download](snippets/gpg.pub){ .md-button }

``` title="curl -O https://drdv.github.io/snippets/gpg.pub"
--8<-- "gpg.pub"
```


``` title="gpg --show-keys --fingerprint --keyid-format=long gpg.pub"
pub   ed25519/69115D75ECD7F803 2025-01-20 [SC] [expires: 2026-01-20]
      Key fingerprint = 4563 0F36 2F40 BB60 AE03  8AF8 6911 5D75 ECD7 F803
uid                            Dimitar Dimitrov <mail.mitko@gmail.com>
sub   cv25519/731BF89E76B1F7FA 2025-01-20 [E] [expires: 2026-01-20]
sub   ed25519/A640370FCD15BADA 2025-01-20 [S] [expires: 2026-01-20]
sub   ed25519/C82ACD166A68F0DF 2025-01-20 [A] [expires: 2026-01-20]
```
