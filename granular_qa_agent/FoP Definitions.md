# FoP (Field of Play) Definitions

This document defines the Field of Play (FoP) classification system used for categorizing Nike and athletic apparel/footwear items by their intended sport or activity context. Each FoP category includes definitions for both Apparel and Footwear where applicable, with sub-sport classifications for more granular categorization.

---

# Deliverable 1

## Sportswear (Apparel) — FoP: `sportswear`

- **Definition:** Lifestyle/casual athletic-inspired apparel for everyday wear; NOT performance.
- **Signals:** lifestyle, casual, streetwear, athleisure, fleece, heritage, classics, originals, essentials.
- **Fabrics:** cotton fleece, French terry, standard cotton jersey (NOT technical performance fabrics).
- **Garments:** hoodies, sweatshirts, crewnecks, joggers/sweatpants, graphic tees, casual track suits, windbreakers (fashion).
- **Exclude:** items with performance fabrics (Dri-FIT, AEROREADY, HeatGear), sport-specific apparel.
- **Examples:** Nike Sportswear Club Fleece Hoodie; Adidas Originals Trefoil Tee; Nike Tech Fleece Joggers; Champion Reverse Weave.

## Sportswear (Footwear) — FoP: `sportswear`

### Sub-sport: `sportswear_running`

- **Definition:** Running-inspired lifestyle/heritage silhouettes; NOT performance running.
- **Franchises:** Nike Air Max (all)/VaporMax/Cortez/Huarache/Shox/Internationalist/Daybreak/P-6000; Adidas NMD/ZX/Ozweego/I-5923; NB 327/574/997/990/2002R; Saucony Jazz/Shadow; On Cloudnova/Cloudrift.
- **Exclude:** performance running terms (track, spikes, trail, marathon, tempo).

### Sub-sport: `sportswear_basketball`

- **Definition:** Basketball-inspired lifestyle sneakers for casual wear.
- **Franchises:** Air Jordan 1-35 (retro); Air Force 1; Nike Dunk (non-SB); Court Vision/Borough; Foamposite; Blazer; Adidas Hoops; Converse All Star/Chuck Taylor; NB 480/550.
- **Exclude:** signature performance lines (LeBron, KD, Curry, etc.), Air Jordan 36+.

### Sub-sport: `sportswear_tennis`

- **Definition:** Court-inspired heritage tennis silhouettes for casual wear.
- **Franchises:** Adidas Stan Smith/Continental 80/Grand Court; Nike Killshot/Court Legacy; Puma GV Special/California; Reebok Club C; NB CT302; Lacoste Carnaby; VEJA Esplar/Campo.
- **Exclude:** performance tennis shoes (Barricade, Vapor, Court Lite).

### Sub-sport: `sportswear_soccer`

- **Definition:** Soccer-inspired terrace/lifestyle sneakers; NOT for playing.
- **Franchises:** Adidas Samba OG/Gazelle/Handball Spezial/City Series (Hamburg, München, etc.); Puma Palermo/Roma; Nike Tiempo '94 Retro.
- **Exclude:** performance cleats (FG/SG/AG), futsal/indoor (IC/TF).

### Sub-sport: `sportswear_skateboarding`

- **Definition:** Skate-inspired lifestyle sneakers; "SB" or "ADV" branding indicates skate.
- **Franchises:** Nike SB Dunk/Janoski/Nyjah/Ishod; Adidas Busenitz/Samba ADV/Forum ADV; Converse CONS; NB Numeric; Vans Old Skool/SK8-Hi (Pro); DC; Etnies; Lakai.
- **Exclude:** non-skate sports.

### Sub-sport: `sportswear_outdoor`

- **Definition:** Outdoor-inspired lifestyle footwear; NOT technical hiking.
- **Franchises:** Nike ACG (casual: Mountain Fly lifestyle, Manoa, Goadome); Hoka Transport.
- **Exclude:** technical hiking boots (use Hiking FoP).

### Sub-sport: `sportswear_other`

- **Use when:** sportswear context is clear but doesn't match above sub-sports.

---

## Running (Apparel) — FoP: `running`

- **Definition:** Performance running apparel with moisture-wicking, breathable, reflective features.
- **Signals:** running, runner, marathon, racer, tempo, pace, distance.
- **Garments:** running singlets/tanks, running shorts (split, racing), running tights/leggings, lightweight running jackets, long sleeve running tops.
- **Design cues:** reflective elements, lightweight moisture-wicking, mesh ventilation, built-in briefs.
- **Exclude:** generic athletic tops (Training), casual running-inspired (Sportswear).
- **Examples:** Nike Dri-FIT Running Top; Adidas Own the Run Singlet; Brooks Sherpa Shorts.

## Running (Footwear) — FoP: `running`

### Sub-sport: `trail_running`

- **Definition:** Performance trail/off-road running shoes.
- **Signals:** trail, off-road, ATR, lugs, Vibram, rock plate.
- **Franchises:** Nike Pegasus Trail/Wildhorse/Kiger/Zegama; Hoka Speedgoat/Torrent/Challenger ATR; Brooks Caldera/Catamount; Saucony Peregrine/Xodus; NB Hierro; On Cloudventure/Cloudultra; ASICS Trabuco/Fuji.
- **Exclude:** road running, hiking boots.

### Sub-sport: `road_running`

- **Definition:** Performance road running for training/racing on paved surfaces.
- **Signals:** road, racer, marathon, tempo, daily trainer.
- **Franchises:** Nike Pegasus (numbered)/Vomero (numbered)/Structure/Invincible/Vaporfly/Alphafly; Adidas Ultraboost (22+)/Adizero/Supernova; Hoka Clifton (numbered)/Bondi/Mach; Brooks Ghost/Glycerin/Adrenaline; ASICS Gel-Kayano/Nimbus/Cumulus; Saucony Endorphin/Triumph/Kinvara; On Cloudmonster/Cloudsurfer.
- **Exclude:** trail (use trail_running), heritage versions (Vomero 5, Ultraboost 1.0 → Sportswear).

### Sub-sport: `track_field_running`

- **Definition:** Spikes and racing shoes for track & field / cross-country.
- **Signals:** track & field, spikes, XC, cross country.
- **Franchises:** Nike Zoom Rival/Victory/Dragonfly/Maxfly; Adidas Adizero Ambition/Prime SP; NB LD5000/MD800/FuelCell MD-X; ASICS Metasprint/Hyper.
- **Exclude:** road/trail running.

### Sub-sport: `running_other`

- **Use when:** clearly performance running but sub-category unclear.

---

## Basketball (Apparel) — FoP: `basketball`

- **Definition:** Basketball-specific performance apparel.
- **Signals:** basketball, hoops, court (basketball context), NBA.
- **Garments:** basketball jerseys/tanks, basketball shorts, warm-up jackets/pants, practice jerseys, compression tights (basketball context).
- **Design cues:** loose fit for range of motion, mesh construction, team/jersey styling.
- **Exclude:** generic training (Training), lifestyle basketball hoodies (Sportswear).
- **Examples:** Nike Basketball Jersey; Jordan Brand Basketball Shorts; Adidas Hoops Warm-Up Jacket.

## Basketball (Footwear) — FoP: `basketball`

### Sub-sport: `signature_basketball`

- **Definition:** Performance basketball shoes tied to specific athletes.
- **Athlete lines:** Nike/Jordan: LeBron, Giannis/Freak, Ja, KD, Kobe/Mamba, Luka, Sabrina, Zion, Tatum, PG; Adidas: Dame, Harden, D.O.N., Trae, Anthony Edwards; Puma: LaMelo MB, Scoot; UA: Curry; NB: Kawhi; ANTA: KAI (Kyrie).
- **Exclude:** lifestyle retro Jordans (1-35), non-basketball.

### Sub-sport: `performance_basketball`

- **Definition:** Non-signature performance basketball (Air Jordan 36+).
- **Pattern:** Air Jordan numbered 36-49 or Roman numerals XXXVI+.
- **Exclude:** AJ 1-35 (Sportswear/sportswear_basketball).

### Sub-sport: `basketball_other`

- **Use when:** clearly performance basketball but sub-category unclear.

---

# Deliverable 2

## Training (Apparel) — FoP: `training`


### Sub-sport: `cross_training`

- **Definition:** Apparel for cross-training/HIIT/lifting/gym workouts requiring durability and range of motion.
- **Signals:** training, workout, gym, cross-train, HIIT, crossfit, lifting, weightlifting, strength.
- **Fabrics:** Dri-FIT, AEROREADY, HeatGear/ColdGear, Speedwick; durable stretch blends.
- **Garments:** training tops/tanks/tees, training shorts, training tights/pants, training jackets, compression gear, sports bras (high-impact).
- **Design cues:** moisture-wicking, reinforced construction, 4-way stretch, supportive/compression fit.
- **Brands/lines:** Nike Pro/Training; Reebok CrossFit; Under Armour Training; Adidas Training.
- **Exclude:** yoga-specific (use `yoga`), running-specific (Running), casual athleisure (Sportswear).
- **Examples:** Nike Pro Training Top; Nike Dri-FIT Training Shorts; Reebok CrossFit Tee; Under Armour HeatGear Compression.

### Sub-sport: `yoga`

- **Definition:** Yoga-specific apparel designed for flexibility, comfort, and freedom of movement during yoga and studio practice.
- **Signals:** yoga, studio, barre, pilates, flow, stretch, mindful movement.
- **Fabrics:** soft, stretchy blends (nylon/spandex); buttery-soft fabrics; Dri-FIT Yoga; Infinalon; Nulu (Lululemon).
- **Garments:** yoga leggings/tights, yoga pants (flare/wide-leg), yoga tops/tanks/bras, yoga bodysuits, wrap tops, cropped hoodies (yoga context).
- **Design cues:** high-stretch 4-way fabric, flatlock seams, high-waisted, second-skin fit, minimal distraction construction.
- **Brands/lines:** Nike Yoga; Lululemon (Align, Wunder); Alo Yoga; Beyond Yoga; Athleta; Manduka; prAna; Sweaty Betty.
- **Exclude:** general gym training (use `training`), casual athleisure (Sportswear), dance-specific (Cheer / Dance).
- **Examples:** Lululemon Align Legging; Nike Yoga Dri-FIT Luxe Tank; Alo Yoga Airlift Bra; Beyond Yoga Spacedye Legging.

### Sub-sport: `training_other`

- **Use when:** training apparel context is clear but doesn't fit `cross_training` or `yoga`.

## Training (Footwear) — FoP: `training`

### Sub-sport: `cross_training`

- **Definition:** Cross-training/HIIT/lifting/multi-direction gym shoes.
- **Signals:** training, workout, gym, cross-train, HIIT, crossfit, lifting, weightlifting.
- **Design cues:** stable/flat base, durable uppers, multidirectional traction; lifters (elevated heel).
- **Franchises:** Nike Metcon/Free Metcon/Romaleos/Legacy Lifter; Reebok Nano/Speed TR; UA TriBase/HOVR Apex; NB Minimus/608; Adidas Dropset/Adipower.
- **Exclude:** running shoes (Running), sport-specific training, lifestyle (Sportswear).
- **Examples:** Nike Metcon 9; Reebok Nano X3; UA TriBase Reign 5.

### Sub-sport: `training_other`

- **Use when:** training context is clear but not enough for `cross_training`.

---

## Soccer (Apparel) — FoP: `soccer`

- **Definition:** Soccer/football-specific performance apparel for pitch play.
- **Signals:** soccer, football (international), futbol, pitch, FIFA, MLS, Premier League, La Liga, kit, jersey.
- **Garments:** soccer jerseys/football shirts, soccer shorts, training tops/pants, pre-match warm-ups, goalkeeper jerseys/pants, soccer socks, tracksuits (soccer context).
- **Design cues:** athletic fit, moisture-wicking polyester, mesh ventilation, team kit styling.
- **Brands/lines:** Nike (Dri-FIT ADV, Strike, Academy, Vapor); Adidas (Tiro, Condivo, Entrada); Puma (teamGOAL, teamFINAL); Umbro; Joma; Hummel; Kappa.
- **Exclude:** casual soccer streetwear (Sportswear), generic training (Training).
- **Examples:** Nike Dri-FIT Strike Soccer Jersey; Adidas Tiro 24 Training Pants; Puma teamGOAL Jersey.

## Soccer (Footwear) — FoP: `soccer`

### Sub-sport: `outdoor_soccer`

- **Definition:** Cleated soccer footwear for FG/SG/AG/MG/HG.
- **Signals:** FG, SG, AG, MG, HG; studs/blades; pitch/field context.
- **Franchises:** Nike Mercurial/Phantom/Tiempo/Premier; Adidas Predator/Copa/X; Puma Future/Ultra/King; NB Furon/Tekela; Mizuno Morelia; Umbro Velocita; Diadora Brasil; Lotto Stadio.
- **Exclude:** indoor/futsal (use `indoor_soccer`), terrace lifestyle (Sportswear/sportswear_soccer).
- **Examples:** Nike Mercurial Vapor 15 FG; Adidas Predator 24.3 FG; Puma Future 1.4 FG/AG.

### Sub-sport: `indoor_soccer`

- **Definition:** Flat or turf-soled futsal/indoor soccer shoes (IC/IN/IT/TF).
- **Signals:** indoor, futsal, sala, IC/IN/IT/TF; non-marking or small-nub outsole.
- **Franchises:** Nike ReactGato/LunarGato/Premier Sala; Adidas Mundial Goal/Top Sala/Copa Tango; NB Audazo; Mizuno Morelia Sala; Joma Top Flex.
- **Exclude:** outdoor cleats, lifestyle Samba/Gazelle (Sportswear/sportswear_soccer).
- **Examples:** Nike ReactGato; Adidas Mundial Team Indoor; Adidas Top Sala.

---

## Hiking / Outdoor (Apparel) — FoP: `hiking`

- **Definition:** Technical outdoor apparel for hiking/trekking; not casual ACG.
- **Signals:** hiking, trek, outdoor, camping, rain/waterproof, GORE-TEX, Storm-FIT, down/insulated, back country.
- **Garments:** waterproof shells, rain pants, down/insulated jackets, hiking pants/shorts, base layers (outdoor), outdoor vests, softshell jackets.
- **Brands/lines:** The North Face, Patagonia, Arc'teryx, Columbia, Marmot; Nike ACG when technical (GORE-TEX).
- **Exclude:** casual outdoor-inspired lifestyle (Sportswear), running windbreakers (Running).
- **Examples:** The North Face Down Parka; Patagonia Torrentshell; Arc'teryx Beta AR; Nike ACG GORE-TEX Jacket.

## Hiking / Outdoor (Footwear) — FoP: `hiking`

- **Definition:** Technical hiking footwear for trail hiking, trekking, backcountry.
- **Signals:** hiking, trekking, backpacking, outdoor, GORE-TEX (GTX), approach shoe.
- **Design cues:** ankle support (boots), Vibram/Contagrip outsoles, aggressive lugs, waterproof membranes, toe caps.
- **Brands/franchises:** Salomon X Ultra/Quest; Merrell Moab/MQM; Keen Targhee; Hoka Anacapa/Kaha; La Sportiva TX/Nucleo; Scarpa Zodiac/Rush; Oboz Bridger/Sawtooth; Danner Trail 2650/Mountain 600; Lowa Renegade; Vasque Breeze; TNF Vectiv; Columbia Newton Ridge; Adidas Terrex Free Hiker.
- **Exclude:** trail running (Running/trail_running), lifestyle outdoor (Sportswear/sportswear_outdoor).
- **Examples:** Salomon X Ultra 5 GTX; Merrell Moab 3 Mid WP; Keen Targhee IV; Lowa Renegade GTX.

---

# Deliverable 3

## Walking (Footwear) — FoP: `walking`

- **Definition:** Walking-specific footwear designed for walking activities.
- **Signals:** walking shoe, walk sneaker, walker.
- **Design cues:** comfort-focused, cushioned, supportive arch, lightweight.
- **Franchises:** Skechers Go Walk/Arch Fit; NB 577/928/Fresh Foam; Brooks Addiction Walker; ASICS Gel-Contend; Hoka Bondi (walking context); Rockport.
- **Exclude:** running shoes (Running), casual sneakers (Sportswear).
- **Examples:** Skechers Go Walk 6; NB 928; Brooks Addiction Walker 2.

---

## Flip Flops (Footwear) — FoP: `flip_flops`

- **Definition:** Flip-flop style sandals with thong strap between toes.
- **Signals:** flip flops, thong sandals.
- **Design cues:** Y-shaped strap between toes, flat sole.
- **Brands:** Reef, Havaianas, Quiksilver, Roxy, Nike Kepa Kai, Adidas Adilette (thong versions), OluKai, Rainbow.
- **Exclude:** slides (Slides), strapped sandals (Outdoor Sandals).
- **Examples:** Reef Fanning; Havaianas Top; Nike Kepa Kai Thong.

---

## Slides (Footwear) — FoP: `slides`

- **Definition:** Slide-on sandals/slippers without back strap.
- **Signals:** slides, slide sandal, recovery slide, slip-on.
- **Design cues:** single/double strap across top, no back strap, slide-on.
- **Brands:** Nike Benassi/Victori One/Offcourt; Adidas Adilette; Oofos OOahh; Hoka Ora Recovery; Crocs Classic Slide; Birkenstock Arizona (slide versions).
- **Exclude:** flip flops (Flip Flops), strapped sandals (Outdoor Sandals).
- **Examples:** Nike Benassi JDI; Adidas Adilette Comfort; Oofos OOahh Recovery Slide.

---

## Outdoor Sandals (Footwear) — FoP: `outdoor_sandals`

- **Definition:** Sandals designed for outdoor/adventure activities with strap systems.
- **Signals:** outdoor sandals, hiking sandals, sport sandals, water sandals.
- **Design cues:** multiple adjustable straps, rugged outsoles, secure fit.
- **Brands:** Teva (Hurricane, Original Universal); Chaco (Z/Cloud, Z/1); Keen (Newport, Clearwater); Merrell; Bedrock.
- **Exclude:** flip flops (Flip Flops), slides (Slides).
- **Examples:** Teva Hurricane XLT2; Chaco Z/Cloud; Keen Newport H2.

---

## Ski & Snowboard (Apparel) — FoP: `ski_snowboard`

- **Definition:** Skiing and snowboarding-specific apparel.
- **Signals:** ski, skiing, snowboard, snowboarding, snow, slopes, resort.
- **Garments:** ski/snowboard jackets, ski/snowboard pants, snow bibs, base layers (snow sports), thermal gear.
- **Design cues:** insulated, waterproof, snow skirts, powder skirts, goggle pockets.
- **Brands:** Burton, The North Face, Patagonia, Columbia, Spyder, Volcom, 686, Oakley.
- **Exclude:** general winter jackets (may be Hiking or Sportswear).
- **Examples:** Burton Snowboard Jacket; TNF Ski Pants; Columbia Snow Bib.

## Ski & Snowboard (Footwear) — FoP: `ski_snowboard`

- **Definition:** Skiing and snowboarding-specific boots.
- **Signals:** ski boots, snowboard boots.
- **Design cues:** rigid shell (ski), soft boot with bindings (snowboard), insulated, snow-specific.
- **Brands:** Salomon, Burton, Rossignol, Atomic, Nordica, K2, DC, Vans (snowboard boots), ThirtyTwo.
- **Exclude:** general winter boots (may be Hiking), snow fashion boots (Sportswear).
- **Examples:** Salomon S/Pro; Burton Moto Boa; Rossignol Alltrack.

---

# Deliverable 4

## Golf (Apparel) — FoP: `golf`

- **Definition:** Golf-specific apparel designed for course wear.
- **Signals:** golf, golfer, course, links.
- **Garments:** golf polos/shirts, golf pants/shorts, golf skirts/skorts, golf jackets/vests, golf rain gear.
- **Design cues:** collar styling, stretch fabrics, UV protection, water-resistant.
- **Fabrics:** Dri-FIT, AEROREADY, Storm-FIT (rain).
- **Brands:** Nike Golf, Adidas Golf, FootJoy, Puma Golf, Under Armour Golf, TravisMathew, Peter Millar, G/FORE, Callaway.
- **Exclude:** generic polos without golf context (Sportswear or Training).
- **Examples:** Nike Dri-FIT Golf Polo; FootJoy Performance Shorts; Adidas Golf Rain Jacket.

## Golf (Footwear) — FoP: `golf`

- **Definition:** Golf-specific footwear for course play.
- **Signals:** golf, golf shoes, spikes, spikeless (golf context).
- **Design cues:** spiked or spikeless outsole, golf-specific traction, waterproof, stable base for swing.
- **Brands/franchises:** FootJoy (Pro/SL, HyperFlex, Premiere, Tour Alpha); Adidas (Tour360, CodeChaos, S2G, Adizero ZG); Nike (Air Zoom Victory/Infinity, Air Max 90 G); Puma (Ignite, ProAdapt); ECCO (Biom); Skechers Go Golf; NB 997 Golf; G/FORE.
- **Exclude:** tennis shoes, lifestyle court shoes (Sportswear).
- **Examples:** FootJoy Pro/SL; Adidas Tour360; Nike Air Zoom Victory Tour.

---

## Tennis (Apparel) — FoP: `tennis`

- **Definition:** Performance tennis apparel for court play.
- **Signals:** tennis, court (tennis context).
- **Garments:** tennis dresses, tennis skirts, tennis tops/tanks, tennis shorts, tennis jackets.
- **Design cues:** athletic fit for court mobility, moisture-wicking, built-in shorts (dresses/skirts), pleated skirts.
- **Fabrics:** Dri-FIT, AEROREADY, HeatGear.
- **Brands:** Nike Court, Adidas Tennis, Lacoste, Wilson, Lotto, Head, Fila.
- **Exclude:** generic athletic dresses/skirts (Training or Sportswear).
- **Examples:** Nike Court Dri-FIT Tennis Dress; Adidas Tennis Skirt; Wilson Tennis Polo.

## Tennis (Footwear) — FoP: `tennis`

- **Definition:** Performance tennis footwear for court play.
- **Signals:** tennis, court (performance context).
- **Design cues:** tennis-specific outsole patterns, lateral support, durability, herringbone traction.
- **Brands/franchises:** Nike (Vapor 12, GP Challenge, Air Zoom); Adidas (Barricade, Ubersonic, Adizero); ASICS (Gel-Resolution, Court FF, Solution Speed); Wilson (Rush Pro); NB (Fresh Foam Lav, 996); Babolat (Jet, Propulse); K-Swiss; Head; Yonex; Lotto (Mirage).
- **Exclude:** lifestyle tennis shoes (Stan Smith, Club C → Sportswear/sportswear_tennis).
- **Examples:** ASICS Gel-Resolution X; Adidas Barricade 13; Nike Vapor 12.

---

## American Football (Apparel) — FoP: `american_football`

- **Definition:** American football-specific apparel.
- **Signals:** football (American context), gridiron, NFL.
- **Garments:** football jerseys, football pants, practice jerseys, compression gear (football context), padded undershirts.
- **Brands:** Nike, Under Armour, Adidas, Riddell.
- **Exclude:** soccer/football international (Soccer).
- **Examples:** Nike Football Jersey; Under Armour Football Practice Shirt.

## American Football (Footwear) — FoP: `american_football`

- **Definition:** American football cleats for turf/grass play.
- **Signals:** football cleats (American), NFL.
- **Design cues:** football-specific cleat pattern, ankle support (mid/high options), durable.
- **Brands/franchises:** Nike (Vapor Edge, Alpha Menace, Force); Under Armour (Highlight, Spotlight); Adidas (Freak, Adizero); NB.
- **Exclude:** soccer cleats (Soccer).
- **Examples:** Nike Vapor Edge Pro 360; Under Armour Highlight MC.

---

## Baseball (Apparel) — FoP: `baseball`

- **Definition:** Baseball-specific apparel.
- **Signals:** baseball, MLB.
- **Garments:** baseball jerseys, baseball pants, practice jerseys, sliding shorts.
- **Brands:** Nike, Under Armour, Majestic, Rawlings, Mizuno.
- **Exclude:** softball (Softball).
- **Examples:** Nike Baseball Jersey; Under Armour Baseball Pants.

## Baseball (Footwear) — FoP: `baseball`

- **Definition:** Baseball cleats (metal or molded).
- **Signals:** baseball, baseball cleats, metal cleats, molded cleats.
- **Design cues:** metal or molded studs, baseball-specific traction.
- **Brands/franchises:** Nike (Alpha Huarache Elite/NXT/Varsity); Under Armour (Harper, Yard); NB (FuelCell 4040, Fresh Foam); Adidas (Icon, Adizero Afterburner); Mizuno.
- **Exclude:** softball (Softball).
- **Examples:** Nike Alpha Huarache Elite 4; NB FuelCell 4040; Under Armour Harper.

---

## Softball (Apparel) — FoP: `softball`

- **Definition:** Softball-specific apparel.
- **Signals:** softball.
- **Garments:** softball jerseys, softball pants, practice jerseys.
- **Brands:** Mizuno, Easton, Under Armour, Nike.
- **Exclude:** baseball (Baseball).
- **Examples:** Mizuno Softball Jersey; Easton Softball Pants.

## Softball (Footwear) — FoP: `softball`

- **Definition:** Softball cleats (typically molded, no metal).
- **Signals:** softball, softball cleats.
- **Design cues:** molded cleats (metal often prohibited), softball-specific traction.
- **Brands:** Mizuno, Nike, Under Armour, Easton, NB.
- **Exclude:** baseball (Baseball).
- **Examples:** Mizuno Finch Elite; Nike Hyperdiamond.

---

# Deliverable 5

## Lacrosse (Apparel) — FoP: `lacrosse`

- **Definition:** Lacrosse-specific apparel.
- **Signals:** lacrosse, lax.
- **Garments:** lacrosse jerseys, lacrosse shorts, practice gear.
- **Brands:** Nike, Under Armour, STX, Warrior, Maverik.
- **Examples:** Nike Lacrosse Jersey; Under Armour Lacrosse Shorts.

## Lacrosse (Footwear) — FoP: `lacrosse`

- **Definition:** Lacrosse cleats.
- **Signals:** lacrosse, lax, lacrosse cleats.
- **Brands/franchises:** Nike (Vapor Lacrosse); NB (Freeze, Rush); Under Armour (Highlight); Warrior; STX.
- **Examples:** Nike Vapor Lacrosse Cleats; NB Freeze v4.

---

## Volleyball (Apparel) — FoP: `volleyball`

- **Definition:** Volleyball-specific apparel.
- **Signals:** volleyball, volley.
- **Garments:** volleyball jerseys, volleyball shorts, spandex shorts.
- **Brands:** Mizuno, ASICS, Nike, Adidas, Under Armour.
- **Examples:** Nike Volleyball Jersey; Mizuno Volleyball Spandex.

## Volleyball (Footwear) — FoP: `volleyball`

- **Definition:** Volleyball-specific court shoes.
- **Signals:** volleyball, volley, indoor court (volleyball context).
- **Design cues:** gum rubber outsoles, lightweight, cushioned for jumping, lateral support.
- **Brands/franchises:** Mizuno (Wave Momentum, Wave Lightning, Wave Dimension); ASICS (Sky Elite FF, Gel-Rocket, Netburner); Nike (Air Zoom Hyperace, Hyperset); Adidas.
- **Examples:** ASICS Sky Elite FF 2; Mizuno Wave Momentum 3; Nike Air Zoom Hyperace 2.

---

## Swimming (Apparel) — FoP: `swimming`

- **Definition:** Swimming-specific training apparel and accessories.
- **Signals:** swimming, swim, pool, aquatic.
- **Garments:** tech suits, swim training tops, swim caps, swim parkas, performance swimwear.
- **Brands:** Speedo, TYR, Arena, Nike Swim.
- **Note:** Basic swimwear (swim trunks, bikinis) typically out-of-scope; this FoP is for performance swim training.
- **Examples:** Speedo Tech Suit; TYR Training Top; Arena Swim Parka.

---

## Cricket (Apparel) — FoP: `cricket`

- **Definition:** Cricket-specific apparel.
- **Signals:** cricket.
- **Garments:** cricket jerseys, cricket whites, cricket pants, cricket sweaters.
- **Brands:** Adidas, New Balance, Gray-Nicolls, Kookaburra, Gunn & Moore.
- **Examples:** Adidas Cricket Jersey; New Balance Cricket Whites.

## Cricket (Footwear) — FoP: `cricket`

- **Definition:** Cricket shoes (spiked or rubber).
- **Signals:** cricket, cricket shoes, cricket spikes.
- **Brands:** Adidas, Puma, New Balance, ASICS, Gray-Nicolls.
- **Examples:** Adidas Howzat Spike; Puma Spike 19.2.

---

## Pickleball (Apparel) — FoP: `pickleball`

- **Definition:** Pickleball-specific apparel.
- **Signals:** pickleball.
- **Garments:** pickleball tops, pickleball shorts/skirts, pickleball dresses.
- **Brands:** Fila, Head, Selkirk, Joola.
- **Examples:** Fila Pickleball Dress; Head Pickleball Shirt.

## Pickleball (Footwear) — FoP: `pickleball`

- **Definition:** Pickleball-specific court shoes.
- **Signals:** pickleball.
- **Design cues:** court shoes, lateral support (similar to tennis but pickleball-specific branding).
- **Brands:** K-Swiss, FILA, Skechers Pickleball, Acacia.
- **Examples:** K-Swiss Express Light Pickleball; FILA Volley Zone Pickleball.

---

# Deliverable 6

## Boxing (Apparel) — FoP: `boxing`

- **Definition:** Boxing-specific apparel.
- **Signals:** boxing, boxer.
- **Garments:** boxing shorts, boxing robes, training gear (boxing context).
- **Brands:** Everlast, Title Boxing, Venum, Ringside, Cleto Reyes.
- **Examples:** Everlast Boxing Shorts; Title Boxing Robe.

## Boxing (Footwear) — FoP: `boxing`

- **Definition:** Boxing boots/shoes.
- **Signals:** boxing, boxing boots, boxing shoes.
- **Design cues:** high-top ankle support, lightweight, thin sole for pivot.
- **Brands:** Nike (Machomai, HyperKO); Adidas (Box Hog); Everlast; Title; Venum; Ringside.
- **Examples:** Nike Machomai 2; Adidas Box Hog 3.

---

## Gymnastics (Apparel) — FoP: `gymnastics`

- **Definition:** Gymnastics-specific apparel.
- **Signals:** gymnastics, gymnast.
- **Garments:** leotards, gymnastics shorts, warm-up suits.
- **Brands:** GK Elite, Under Armour, Adidas, Nike.
- **Examples:** GK Elite Leotard; Nike Gymnastics Warm-Up.

---

## Cheer / Dance (Apparel) — FoP: `cheer_dance`

- **Definition:** Cheerleading and dance-specific apparel.
- **Signals:** cheer, cheerleading, dance, dancer.
- **Garments:** cheer uniforms, cheer shells/skirts, dance outfits, practice wear.
- **Brands:** Varsity Spirit, Nike Cheer, Motionwear.
- **Examples:** Varsity Spirit Cheer Uniform; Nike Cheer Practice Top.

## Cheer / Dance (Footwear) — FoP: `cheer_dance`

- **Definition:** Cheerleading and dance-specific shoes.
- **Signals:** cheer, cheerleading shoes, dance shoes.
- **Design cues:** lightweight, flexible, supportive for stunts/jumps.
- **Brands:** Nfinity (Vengeance, Flyte); Nike (Cheer Sideline); Varsity; Rebel.
- **Examples:** Nfinity Vengeance; Nike Cheer Sideline IV.

---

## Rugby (Apparel) — FoP: `rugby`

- **Definition:** Rugby-specific apparel.
- **Signals:** rugby.
- **Garments:** rugby jerseys, rugby shorts, rugby training gear.
- **Brands:** Canterbury, Adidas, Nike, Under Armour, Kooga.
- **Examples:** Canterbury Rugby Jersey; Adidas Rugby Shorts.

## Rugby (Footwear) — FoP: `rugby`

- **Definition:** Rugby boots/cleats.
- **Signals:** rugby, rugby boots.
- **Design cues:** rugby-specific studs, ankle support.
- **Brands:** Adidas (Kakari, Malice); Canterbury (Phoenix, Stampede); Nike; Mizuno.
- **Examples:** Adidas Kakari Elite SG; Canterbury Phoenix 4.0.

---

## Wrestling (Apparel) — FoP: `wrestling`

- **Definition:** Wrestling-specific apparel.
- **Signals:** wrestling, wrestle, wrestler.
- **Garments:** wrestling singlets, wrestling gear.
- **Brands:** ASICS, Nike, Adidas, RUDIS, Cliff Keen.
- **Examples:** ASICS Wrestling Singlet; Cliff Keen Singlet.

## Wrestling (Footwear) — FoP: `wrestling`

- **Definition:** Wrestling shoes for mat competition.
- **Signals:** wrestling, wrestling shoes, mat shoes.
- **Design cues:** high-top ankle support, grippy sole for mat, snug fit, lightweight.
- **Brands/franchises:** ASICS (Aggressor, Matflex, Snapdown, MatControl); Nike (Inflict, Fury, Freek, Tawa); Adidas (Mat Wizard, Combat Speed, Tech Fall, HVC); RUDIS.
- **Examples:** ASICS Aggressor 4; Nike Inflict 3; Adidas Mat Wizard.

---

## Field Hockey (Apparel) — FoP: `field_hockey`

- **Definition:** Field hockey-specific apparel.
- **Signals:** field hockey, hockey (field context).
- **Garments:** field hockey jerseys, field hockey skirts/shorts.
- **Brands:** Adidas, Grays, TK Hockey, Kookaburra.
- **Exclude:** ice hockey (out-of-scope).
- **Examples:** Adidas Field Hockey Jersey.

## Field Hockey (Footwear) — FoP: `field_hockey`

- **Definition:** Field hockey shoes.
- **Signals:** field hockey, hockey (field context).
- **Brands:** Adidas (Lux, Fabela); ASICS; Grays; TK.
- **Exclude:** ice hockey skates (out-of-scope).
- **Examples:** Adidas Lux 2.0 Field Hockey.

---

# Glossary

**Soccer Surface Codes:**

- **FG:** Firm Ground – molded studs for natural grass.
- **SG:** Soft Ground – longer/metal studs for wet/muddy grass.
- **AG:** Artificial Ground – shorter studs for artificial grass (3G/4G).
- **MG:** Multi-Ground – versatile stud plate (FG + AG).
- **HG:** Hard Ground – short studs for hard surfaces.
- **IC/IN:** Indoor Court – flat non-marking outsole.
- **TF:** Turf – small rubber nubs for synthetic turf.
- **IT:** Indoor Training/Turf – similar to IC/TF.

**Outdoor/Hiking Terms:**

- **ACG:** All Conditions Gear (Nike) – Hiking when technical, Sportswear when casual.
- **GTX:** GORE-TEX – waterproof breathable membrane.
- **Vibram:** Premium outsole brand.
- **Contagrip:** Salomon's proprietary outsole.
