# Implementacija Swarm algoritma u programskom jeziku Python

**1. Predlog problema:**
Vodjenje čestica ka unutrašnjosti trougla u 2d prostoru, očekuje se da posle odredjenog broja iteracija sve čestice budu unutar granica proizvoljnog trougla. Tačka ka kojoj se teži je **centralna tačka trougla** iliti *"triangle centroid"*. Unose se koordinate tri tačke koje će činiti trougao, sa druge strane, sve čestice dobijaju nasumično mesto na početku algoritma. Zadatak se sastoji u napredovanju čestica kroz prostor sve do unutrašnjosti trougla i ciljane tačke.

**2. Problem za primenu Swarm algoritma:**


**3. Implementacija Swarm algoritma:**


**3.1. Parametri Swarm algoritma:**
Svi ulazni argumenti algoritma su parametrizovani.

1. **w_inertia** -  (0.5)
2. **c_cognitive** -  (1)
3. **c_social** -  (2)
4. **num_particles** -  (40)
5. **num_iterations** -  (25)

Na slikama se može videti napredovanje algoritma. Polazni skup čestica je nasumično generisan i njihove koordinate imaju neodredjene varijacije u odnosu na jednu centralnu tačku prostora koja nije unutar trougla. Svakom iteracijom dobija se skup čestica koje napreduju ka trouglu, sve dok ne probiju nejgove granice i zadrže se unutar linija. Na kraju se očekuje skup čestica koje s unutar trougla i što je moguće više se poklapaju sa centrom težipta trougla. Mera kvaliteta čestice meri se njenom udaljenošću od ciljane tačke.
 
![alt text][screenshot_algotithm_start]

[screenshot_algotithm_start]: metadata/algorithm-start.jpg

U konzolnom prozoru se nakon svake iteracije prikazuje stepen greške najboljeg rešenja, odnosno najkvalitetnije čestice. Na kraju algoritma može se videti globalna pozicija najbolje čestice u 2d prostoru kao i njen stepen greške.

![alt text][screenshot_algotithm_mid1]

[screenshot_algotithm_mid1]: metadata/algorithm-mid1.jpg

![alt text][screenshot_algotithm_mid2]

[screenshot_algotithm_mid2]: metadata/algorithm-mid2.jpg

![alt text][screenshot_algotithm_end]

[screenshot_algotithm_end]: metadata/algorithm-end.jpg

## Implementacioni detalji



### Primer napredovanja čestica kroz iteracije

Primer napredovanja hromozoma će biti prikazan u nastavku. Biće razmatran i-ti hromozom prve i poslednje generacije. U prilogu se može videti kodirani hromozom na početku algoritma, ovo je nasumično generisani niz pomeraja. Prva polovina vrednosti se odnosi na pomeraje po x-osi, ostatak na odgovarajuće pomeraje po y-osi.