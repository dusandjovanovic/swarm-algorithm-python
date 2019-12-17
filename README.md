# Implementacija Swarm algoritma u programskom jeziku Python

**1. Predlog problema:**
Vodjenje čestica ka unutrašnjosti trougla u 2d prostoru, očekuje se da posle odredjenog broja iteracija sve čestice budu unutar granica proizvoljnog trougla. Tačka kojoj se teži je **centralna tačka trougla** iliti *"triangle centroid"*. Unose se koordinate tri tačke koje će činiti trougao, sa druge strane, sve čestice dobijaju nasumično mesto na početku algoritma. Zadatak se sastoji u napredovanju čestica kroz prostor sve do unutrašnjosti trougla i krajnje tačke.

**2. Problem za primenu Swarm algoritma:**
Osnovni problem je u činjenici da se postavljeni zadatak velikim centralizovanim sistemom ne može rešiti na lak način. Swarm sistem koji se bazira na prostim pravilima svake čestice bez centralizovane kontrole je jako pogodan za ovakvu postavku problema. Čestice imitiraju ponašanje insekata i interaguju medjusobno (uče jedne od drugih) pa se samim tim postepeno približavaju cilju.

Ovaj algoritam ne garantuje nalaženje globalnog minimuma (minimalna mera greške) ali se pokazuje jako dobro u nekontinuiranim okruženjima, po potrebi i višedimenzionalnim.

**3. Implementacija Swarm algoritma:**
Za implementaciju algoritma koriste se samo osnovne biblioteke Python okruženja. S obzirom na složenost problema nije neophodno koristiti open-source biblioteke. Predstavljanje čestica, kao i sve funkcije mere grešaka i učenja izgradjene su od osnovnih biblioteka što dozvoljava veću fleksibilnost.

Osnovni pregled: **k-ta iteracija** algortima, **k+1** je sledeća iteracija:

*x^i(k+1) = x^i(k) + v^i(k) + 1*

Brzina čestice (velocity):

*v^i(k) + 1 = w(k)v^i(k) + c(1)r(1)(p^i(k) − x^i(k)) + c(2)r(2)(p^g(k) − x^(i)k)*
1. **x^i(k)** - pozicija čestice
2. **v^i(k)** - brzina čestice
3. **p^i(k)** - najbolja individualna pozicija čestice
4. **p^g(k)** - najbolja globalna pozicija od svih čestica swarm-a
5. **c(1), c(2)** - kognitivni i socijalni parametri
5. **w(1), w(2)** - nasumične vrednosti

Iz jednačine brzine mogu se primetiti dva člana: **socijalni član i kognitivni član**. Socijalni se oslanja na najbolju globalnu poziciju, dok se kognitivni računa na osnovu najbolje individualne pozicije.

**3.1. Parametri Swarm algoritma:**
Svi ulazni argumenti algoritma su parametrizovani. Početak algoritma sastoji se od inicijalizacije svih vredosti, nasumičnog generisanja početnih koordinata svih čestica kao i njihovih parametara brzina.

1. **w_inertia** - konstanta inercije, koliko uzimati u obzir prethodnu poziciju (0.5)
2. **c_cognitive** - kognitivna konstanta, koliko uzimati u obzir najbolju individualnu poziciju (1)
3. **c_social** - socijalna konstanta, koliko uzimati u obzir najbolju globalnu poziciju (2)
4. **num_particles** - broj čestica jednog swarm-a (40)
5. **num_iterations** - broj dozvoljenih iteracija (25)

Nakon inicjalizacija prelazi se na iteracije algoritma. Kroz svaku iteraciju se za čestice traži povratna vrednost **funckije procene cene - cost_function(position)**, u zavisnosti od trenutne pozicije čestice i ciljne tačke. Ukoliko je novonastala procena manja od individualne ili globalne najbolje vrednosti dolazi do njihovih promena. U svakoj iteraciji se menjaju pozicije i brzine svih čestica. Takodje, ako dodje do zadovoljavanja uslova minimalne dozvoljene greške prekidaju se preostale iteracije.

Osnovni koncept se bazira na balansu izmedju prethodne pozicije čestice, udaljenosti od najbolje individualne pozicije (kognitivna sila) i udaljenosti od najbolje globalne pozicije (socijalna sila).

Na slikama se može videti napredovanje algoritma. Polazni skup čestica je nasumično generisan i njihove koordinate imaju neodredjene varijacije u odnosu na jednu centralnu tačku prostora koja nije unutar trougla. Svakom iteracijom dobija se skup čestica koje napreduju ka trouglu, sve dok ne probiju nejgove granice i zadrže se unutar linija. Na kraju se očekuje skup čestica koje su unutar trougla i što je moguće više se poklapaju sa centrom težišta trougla. Mera kvaliteta čestice meri se razdaljinom od ciljane tačke.
 
![alt text][screenshot_algotithm_start]

[screenshot_algotithm_start]: metadata/algorithm-start.jpg

U konzolnom prozoru se nakon svake iteracije prikazuje stepen greške najboljeg rešenja, odnosno najkvalitetnije čestice. Na kraju algoritma može se videti globalna pozicija najbolje čestice u 2d-prostoru kao i njen stepen greške.

![alt text][screenshot_algotithm_mid1]

[screenshot_algotithm_mid1]: metadata/algorithm-mid1.jpg

![alt text][screenshot_algotithm_mid2]

[screenshot_algotithm_mid2]: metadata/algorithm-mid2.jpg

![alt text][screenshot_algotithm_end]

[screenshot_algotithm_end]: metadata/algorithm-end.jpg

## Implementacioni detalji

Klasa koja sadrži potrebna ponašanja nazvana je `Particle`, a njene metode su:

1. `__init__` za inicijalizaciju parametara
2. `evaluate` za evaluaciju dobrote čestice
3. `update_position` za promenu pozicije čestice na osnovu nove vrednosti brzine
4. `update_velocity` za promenu brzine čestice

Pomoćne metode:

1. `cost_function` za meru cene/greške, manje vrednosti su bolje
2. `particle_swarm` za inicijalizaciju grupa čestica i iteracije

### Inicijalizacija i metoda `__init__`

Na početku ciklusa jedne čestice neophodno je inicjalzivati sve njene parametre i početnu lokaciju. Ova metoda postavlja prazne parametre koji su neophodni za dalje korake, ovo podrazumeva brzinu, poziciju i slično. Inicijalno se početne lokacije tačaka u 2d-prostoru nasumično generišu, početne brzine su takodje nasumične.

```python
for i in range(0, num_dimensions):
            self.velocity_i.append(uniform(-1, 1))
            self.position_i.append(x0[i] + random())
```

### Evaluacija i metoda `evaluate`

Metoda procene/evaluacije je neophodna i stalno se primenjuje nad svim česticama. Koristi pomoćnu metodu `cost_function` kojom se dobija mera greške čestice, odnosno njena dobrota. Ovde se vrši i provera da li je trenutna pozicija čestice najbolja u swarm-u i na osnovu toga se po potrebi menjaju individualni parametri čestice `position_i_best` i `error_i_best`.

```python
def evaluate(self, costFunc):
        self.error_i = costFunc(self.position_i)
        if self.error_i < self.error_i_best or self.error_i_best == -1:
            self.position_i_best = self.position_i.copy()
            self.error_i_best = self.error_i
```

### Promena pozicije i metoda `update_position`

Nakon promene vrednosti brzine čestice neophodno je shodno njoj promeniti i trenutnu poziciju. Da bi se smanjila mogućnost lutanja čestica u prostoru prate se i unapred zadate granice.

```python
def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]

            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            if self.position_i[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]
```

### Promena brzine i metoda `update_velocity`

U svakoj iteraciji dolazi do promene brzina čestica po prethodno pomenutoj formuli. Metoda `update_velocity` se bavi ovime. Pritom se uzimaju u obzir vrednosti postavljenih koordinata inercije, kao i socijalne i kognitivne sile.

```python
def update_velocity(self, position_g_best):
    for i in range(0, num_dimensions):
        r1, r2 = random(), random()
        vel_cognitive = c_cognitive * r1 * (self.position_i_best[i] - self.position_i[i])
        vel_social = c_social * r2 * (position_g_best[i] - self.position_i[i])
        self.velocity_i[i] = w_inertia * self.velocity_i[i] + vel_cognitive + vel_social
```


### Mera greške i metoda `cost_function`

Ova pomoćna metoda je neophodna u svakoj iteraciji i uzima u obzir trenutne (x, y) koordinate čestice. `triangle_centroid` su koordinate centra trougla (formirane prethodno). Potrebno je na osnovu udaljenosti čestice od ciljne tačke formirati procenu cene, odnosno meru greške. Manje vrednosti se očekivano smatraju boljim.

```python
def cost_function(x):
    distance_to_goal = numpy.sqrt((triangle_centroid[0] - x[0]) ** 2 + (triangle_centroid[1] - x[1]) ** 2)
    return distance_to_goal
```


### Algoritam i metoda `particle_swarm`

Ovo je osnovna metoda koja omogućava algoritam i napredovanje kroz iteracije. Na početku se inicjalizuje početni skup svih čestica, kao i globalne vrednosti najmanje greške i koordinata najbolje pozicionirane čestice.

U svakoj iteraciji **dolazi do evaluacije svih čestica**, zatim i **promene globalnih vrednosti** ukoliko je to potrebno shodno poslednjoj evaluaciji. Sve čestice **trpe promene brzina i trenutnih pozicija**, sve promene se zatim prikazuju na grafiku 2d prostora. Pored vodjenja evidencija čestica, na grafiku se prikazuje i najbolja globalna pozicija.

```python
error_g_best = -1
position_g_best = []

swarm = []
for i in range(0, num_particles):
    swarm.append(Particle(x0))

...

i = 0
while i < maxiter:
    print(f'iteration: {i:>4d}, best solution: {error_g_best:10.6f}')
    ...
    for j in range(0, num_particles):
        swarm[j].evaluate(costFunc)
        if swarm[j].error_i < error_g_best or error_g_best == -1:
            position_g_best = list(swarm[j].position_i)
            error_g_best = float(swarm[j].error_i)

    for j in range(0, num_particles):
        swarm[j].update_velocity(position_g_best)
        swarm[j].update_position(bounds)
        ...
    ...
    i += 1

...
```

### Primer napredovanja čestica kroz iteracije

Primer napredovanja čestice će biti prikazan u nastavku. Biće razmatran skup nakon prve i poslednje iteracije. U prilogu se može videti skup vrednosti pozicija i brzina čestica kao i promene koje su čestice pretrpele izmedju iteracija algoritma. Zbog velikog broja podataka prikazano je na primeru samo prve čestice iz swarm skupa.

```json
{
    "swarm": [{
        error_i:	3.5567915301528563,
        error_i_best:	3.5567915301528563,
        position_i:	[0.9581224128162724, 2.5284571904175372],
        position_i_best:	[0.7238504823196498, 3.111126082879543],
        velocity_i:	[0.23427193049662265, -0.5826688924620057]
    }]
```

```json
{
    "swarm": [{
        error_i:	0.004096218913725794,
        error_i_best:	0.004096218913725794,
        position_i:	[-1.0166652560790046, 0.005918579715854832],
        position_i_best:	[-1.0021849423375173, 0.0034648284764024467],
        velocity_i:	[-0.014480313741487186, 0.002453751239452385]
    }]
```
