#import logging
from tipfy import (RequestHandler, RequestRedirect, Response, abort,
    cached_property, redirect, redirect_to, url_for)
from apps.stonewareglazes.Model import IndexItem, Page, TocItem

class UpdatePageHandler(RequestHandler):
    def get(self, **kwargs):
        pages = Page.all()
        for page in pages:
            if (page.sequenceNumber >=49) and (page.sequenceNumber < 222):
                page.loginRequired = True
            else:
                page.loginRequired=False
            page.put()
        response = redirect_to('admin')
        response.data = ''
        return response
    
class LoadTocHandler(RequestHandler):
    def get(self, **kwargs):
        items=[
               [1,"", "CONTENTS",""],
               [3,"", "FOREWORD",""],
               [3,"", "EXPLANATORY OUTLINE",""],
               [5,"", "Practical Guide.",""],
               [5,"", "Base glazes - a key to understanding glaze principles.",""],
               [5,"", "Limits. ",""],
               [5,"", "Methodology.",""],
               
               [2,"", "PART I BASE GLAZES",""],
              
               [3,"1", "PREPARATIONS","2"],
               [5,"", "Introduction. ",""],
               [5,"", "Group study. ",""],
               [5,"", "Reference books. ",""],
               [5,"", "Base glaze theory and practice. ",""],
               [5,"", "Raw materials. ",""],
               [5,"", "Guidelines for selection of materials.",""],
               
               [3,"2", "BASIC CHEMISTRY","10"],

               [5,"", "Atoms. ",""],
               [5,"", "Molecules. ",""],
               [5,"", "Oxides. ",""],
               [5,"", "Glaze - a glassy mix of oxides. ",""],
               [5,"", "The relationship between recipe, oxide weight % and Seger formula. ",""],
               [5,"", "Converting a Seger formula to oxide weight %. ",""],
               [5,"", "Converting a Seger formula to a recipe. ",""],

               [3,"3","GETTING STARTED -- MATERIAL REQUIREMENTS","16"],
               [5,"", "Glaze materials. ",""],
               [5,"", "Clay materials.  ",""],
               [5,"", "Equipment and books.",""],

               [3,"4", "LINE BLENDS - ASH, CLAY AND ROCK GLAZES ","20"],
               [5,"", "Wood ash.  ",""],
               [5,"", "Clay.  ",""],
               [5,"", "Rock dust.  ",""],
               [5,"", "Ball Mills.  ",""],
               [5,"", "Volumetric blending - a lot of glazes with a little work.  ",""],
               [5,"", "References. ",""], 

               [3,"5", "BASELINE GRIDS AND BIAXlAL BLENDS","25"],
               [5,"","Baseline grids. ",""],
               [5,"","Biaxial blends.",""],
               
               [3,"6","EXPERIMENTAL PROCEDURE FOR BIAXIAL BLENDS","28"],
               [5,"", "Making the glazes. Applying the glazes and oxides and firing.",""],
               [5,"", "Assessment tiles and individual tiles.",""],
               [5,"", "Putting the results in order.",""],
               [5,"", "Assessment of results.",""],

               [3,"7", "ALUMINA AND SILICA IN STONEWARE GLAZES","36"],
               [5,"", "Effects of varying alumina and silica.",""],
               [5,"", "Sources of alumina in glazes.",""],
               [5,"", "Sources of silica in glazes.",""],
               [5,"", "The alumina/silica ratio.",""],

               [3,"8", "LIME ALKALI GLAZES","43"],
               [5,"", "The use of calcium in stoneware glazes.",""],
               [5,"", "Sources of calcium.",""],
               [5,"", "The use of alkali fluxes in stoneware glazes.",""],
               [5,"", "Sources of alkalis.",""],
               [5,"", "Preliminary comments on experiments.",""],
               [5,"", "The 0.9 Limestone Set.",""],
               [5,"", "The 0.8 Limestone Set. ",""],
               [5,"", "The 0.7 Limestone Set. ",""],
               [5,"", "The 0.6 Limestone Set. ",""],
               [5,"", "The 0.6 Feldspar Set.",""],

               [3,"9", "MAGNESIUM GLAZES","62"],
               [5,"", "Sources of magnesia. ",""],
               [5,"", "The Magnesium Set. ",""],
               [5,"", "Alternative recipes for the Magnesium Set. ",""],
               [5,"", "Intermediate sets.",""],

               [3,"10", "ZINC GLAZES","68"],
               [5,"", "Sources of zinc. ",""],
               [5,"", "The Zinc Set. ",""],
               [5,"", "Intermediate sets.",""],

               [3,"11","BARIUM GLAZES","74"],
               [5,"", "Sources of barium. ",""],
               [5,"", "Barium carbonate is poisonous. ",""],
               [5,"", "Intermediate sets. ",""],
               [5,"", "The Barium Set. ",""],
               [5,"", "The Barium Alkaline Set.",""],
               
               [3,"12", "DESIGNING AN EXPERIMENT","82"],
               [5,"", "Design your own base glaze experiment.",""],

               [3,"13", "PHASE EQUILIBRIA DIAGRAMS AND EUTECTICS","84"],
               [5,"", "Simple phase equilibria diagrams. ",""],
               [5,"", "More complicated P.E. diagrams. ",""],
               [5,"", "Triaxial diagrams. ",""],
               [5,"", "The effect of increasing the number of ingredients.",""],
               [5,"", "Reading triaxial phase diagrams.",""],
               [5,"", "Summary. ",""],
               [5,"", "References.",""],
               
               [3,"14", "CALCULATIONS","92"],
               [5,"", "Converting formula to recipe. ",""],
               [5,"", "The Four Question technique. ",""],
               [5,"", "Percentage calculation. ",""],
               [5,"", "Formula to recipe - model conversion. ",""],
               [5,"", "Exercises. ",""],
               [5,"", "List of raw materials. ",""],
               [5,"", "Conversion of a glaze recipe to a Seger formula. ",""],
               [5,"", "Conversion of analysis data (%) to Seger formula and molecular weight. ",""],
               [5,"", "Formula to recipe - a more difficult example. ",""],
               [5,"", "Simultaneous Equations. ",""],
               [5,"", "The percentage method of glaze calculation. ",""],
               [5,"", "More formula to recipe. ",""],
               [5,"", "Calcining calculations. ",""],
               [5,"", "Parts chart calculations. ",""],
               [5,"", "Partial blends and intermediate blends. ",""],
               [5,"", "Calculating blended glaze recipes.",""],
               
               [2,"", "PART II	SPECIFIC GLAZES",""],

               [3,"15", "METHODOLOGY","120"],
               [5,"", "Outline. ",""],
               [5,"", "A reference framework for molecular formulae. ",""],
               [5,"", "Test firings. ",""],
               [5,"", "Draw trials. ",""],
               [5,"", "Oxidation - neutral - reduction atmospheres. ",""],
               [5,"", "Mortar and pestle line blending technique.",""],
               
               [3,"16", "CRYSTALLINE GLAZES","124"],
               [5,"", "Devitrification - glass giving rise to crystals. ",""],
               [5,"", "The process of crystallisation. ",""],
               [5,"", "Important factors in crystal growth. ",""],
               [5,"", "Different types of crystalline glazes. ",""],
               [5,"", "Exercises. ",""],
               [5,"", "References.",""],

               [3,"17", "MATT GLAZES","134"],
               [5,"", "Introduction. ",""],
               [5,"", "The clay-glaze interface. ",""],
               [5,"", "Exercises: Flux Matts. Alumina matts. Silica matts. ",""],
               [5,"", "References.",""],

               [3,"18", "OPAQUE GLAZES. CHUN-BLUE GLAZES","141"],
               [5,"", "Introduction. ",""],
               [5,"", "Opaque glazes. ",""],
               [5,"", "Chun-blue glazes. ",""],
               [5,"", "The chun-blue effect. ",""],
               [5,"", "Factors affecting the development of chun-blue. ",""],
               [5,"", "Chun-type glaze recipes. References. ",""],
               
               [3,"19", "DECORATED WHITEWARE. GLAZE FIT","150"],
               [5,"", "Introduction. ",""],
               [5,"", "Whiteness - how will you get it? ",""],
               [5,"", "Body.",""],
               [5,"", "White slip. ",""],
               [5,"", "Colours. ",""],
               [5,"", "Glazes. ",""],
               [5,"", "Glaze fit. ",""],
               [5,"", "References.",""],
               
               [3,"20", "HIGH IRON GLAZES","158"],
               [5,"", "Introduction. ",""],
               [5,"", "Forms of iron oxide in glazes. ",""],
               [5,"", "Unity formula convention for iron glazes. ",""],
               [5,"", "Experiments. ",""],
               [5,"", "Discussion of results including iron solubility, rust break, chun-blue occurrence and teadust crystals. ",""],
               [5,"", "Specific iron glazes, including honey, tenmoku, kaki, oilspot tenmoku, teadust, tomato red and tessha glazes, and iron glazes using natural materials. ",""],
               [5,"", "References. ",""],
               [5,"", "High iron Stoneware Glazes' by R. R. Hughan.",""],
               
               [3,"21", "CELADON","173"],
               [5,"", "Introduction. ",""],
               [5,"", "The base glaze - its role in celadon glazes. ",""],
               [5,"", "Lung Chuan celadon. ",""],
               [5,"", "Blue celadon. ",""],
               [5,"", "Bubbles in celadon. ",""],
               [5,"", "References.",""],
               
               [3,"22", "KUAN GLAZES","179"],
               [5,"", "Description and the problems involved. ",""],
               [5,"", "Suggested research program. ",""],
               [5,"", "References.",""],

               [3,"23", "SHINO GLAZES","183"],
               [5,"", "Traditional Japanese Shino. ",""],
               [5,"", "Nepheline syenite Shino.",""],
               [5,"", "'Fire colour' in Shino. ",""],
               [5,"", "Technical notes. ",""],
               [5,"", "References.",""],

               [3,"24", "COPPER GLAZES","188"],
               [5,"", "Copper as a colourant. ",""],
               [5,"", "Oxidised copper glazes. ",""],
               [5,"", "Reduced copper glazes - copper reds. ",""],
               [5,"", "References.",""],

               [3,"25", "NATURAL GLAZES FROM WOODFIRING","194"],
               [5,"", "Introduction. ",""],
               [5,"", "Typical Shigaraki climbing kiln. ",""],
               [5,"", "Using a smaller kiln. ",""],
               [5,"", "A Bizen Kiln. ",""],
               [5,"", "A few hints. ",""],
               [5,"", "Extended firings - glazed and unglazed pots. ",""],
               [5,"", "Ash types and clay types. ",""],
               [5,"", "References.",""],

               [3,"26", "ROCK GLAZES","200"],
               [5,"", "Igneous rocks. ",""],
               [5,"", "Identifying rocks and minerals. ",""],
               [5,"", "Crushing and grinding the rock. ",""],
               [5,"", "Ivan Englund on rock glazes. ",""],
               [5,"", "Some simple testing procedures. ",""],
               [5,"", "References. ",""],
               [5,"", "Extract: 'Borax Bead Test'.",""],

               [3,"", "INDEX","209"],
	       ]

               
        seq=0
        for i in items:
            seq=seq+10
            #logging.debug("attempting: " + i[0])
            item= TocItem()
            item.styleNumber=i[0]
            item.blockHeading=i[1]
            item.label=i[2]
            item.pageNumber=i[3].upper()
            item.sequenceNumber=seq
            item.put()
        response = redirect_to('admin')
        response.data = ''
        return response

class LoadIndexHandler(RequestHandler):
    def get(self, **kwargs):
        items = [
                    ["A.F.A.S.", "ix"],
                    ["alkali fluxes", "5, 44"],
                    ["alumina", "36"],
                    ["alumina matts", "139" ],
                    ["alumina/silica ratio", "41" ],
                    ["alumina, sources of", "40"],
                    ["anagama", "184, 194" ],
                    ["analysis sheets", "4"],
                    ["anorthite", "13, 92" ],
                    ["application of glazes", "xiii" ],
                    ["ash, analyses", "199" ],
                    ["ash glazes, natural", "194" ],
                    ["ash, wood", "20, 194" ],
                    ["ash, preparation", "20" ],
                    ["assessment of results", "35" ],
                    ["assessment tiles", "17, 31, 32"],
                    ["assessment tiles, firing of", "31" ],
                    ["atoms", "10"],
                    ["'avbas'", "203" ],
                    ["aventurine glaze", "129"],
                    ["'avgran'", "203"],
                    
                    ["ball clay Q.A.", "101, 103 "],
                    ["ball mills", "21"],
                    ["BaO in celadons", "175 "],
                    ["BaO in iron glazes", "164 "],
                    ["barium carbonate, poisonous nature of", "74"],
                    ["barium glazes", "74 "],
                    ["barium matts", "136 "],
                    ["barium, sources of", "74 "],
                    ["baseline", "25 "],
                    ["baseline grid", "25 "],
                    ["biaxial blends", "26, 28, 29 "],
                    ["bizen clay", "194 "],
                    ["bizen firing", "196 "],
                    ["black Seto ware", "183"],
                    ["blended glaze recipes, calculation of", "116 "],
                    ["borax", "44 "],
                    ["borax bead test", "202, 207 "],
                    ["boric oxide, effect on copper red glazes", "190"],
                    ["Broken Hill feldspar", "103"],

                    ["calcining calculations", "110 "],
                    ["calcite", "7 "],
                    ["calcium matts", "139 "],
                    ["CaO in glazes", "43 "],
                    ["celadon", "163, 173 "],
                    ["celadon, blue", "175, 177 "],
                    ["celadon, bubbles in", "178 "],
                    ["celadon, effect of base glaze on", "173"],
                    ["celadon, Lung Chuan", "175 "],
                    ["cha-no-yu", "183, 194 "],
                    ["chrome red glaze", "144 "],
                    ["Chun-blue", "49, 53, 71, 145 "],
                    ["Chun-blue, factors affecting", "145"],
                    ["Chun-blue in iron glazes", "165"],
                    ["clay-glaze interface", "135 "],
                    ["colloidal silica", "146 "],
                    ["colourless iron", "164, 170 "],
                    ["conversion chart", "92 "],
                    ["conversion factor", "165 "],
                    ["copper glazes", "188 "],
                    ["copper red glazes", "189 "],
                    ["copper red glazes, firing of", "191"],
                    ["copper ruby", "189 "],
                    ["corner glazes", "xii "],
                    ["crazing", "38, 156 "],
                    ["cristobalite", "157 "],
                    ["crystal growth", "126 "],
                    ["crystallisation, process of", "125"],
                    ["crystals", "49, 53, 65, 71, 124"],

                    ["data", "xiv, 45 "],
                    ["devitrification", "124 "],
                    ["dolomite", "7, 62, 65 "],
                    ["draw trials", "121"],

                    ["engobes", "151,153 "],
                    ["eutectic", "84 "],
                    ["eutectic composition", "84 "],
                    ["eutectic temperature", "84"],
                    ["eutectic trough", "90 "],
                    ["experiments, preliminary comments to", "45"],

                    ["feldspar", "5, 8 "],
                    ["ferric chloride", "186 "],
                    ["ferrous silicate", "147 "],
                    ["fire colour in Shino glazes", "183, 184, 186"],
                    ["firing", "xiii"],
                    ["firings for base glaze sets", "47 "],
                    ["flambe glaze", "189, 192 "],
                    ["flux-alumina matts", "37 "],
                    ["fluxes, diversification of", "91 "],
                    ["flux matts", "37, 136 "],
                    ["four question technique", "92 "],
                    ["frits, alkaline", "5"],


                    ["glaze fit", "38, 156 "],
                    ["grey Shino", "184 "],
                    ["group study", "2"],


                    ["Hidasuki markings", "197"],
                    ["honey glaze, see Chapter 20","158"],


                    ["igneous rocks", "200 "],
                    ["individual tiles", "17, 33, 34 "],
                    ["interface, clay-glaze", "135 "],
                    ["intermediate blends", "115 "],
                    ["iron chloride", "186 "],
                    ["iron, colourless", "164, 170 "],
                    ["iron glazes", "158 "],
                    ["iron oxide, forms of", "158, 170 "],
                    ["iron oxide, solubility of", "164 "],
                    ["iron silicate", "177 "],
                    ["isotherm", "90"],


                    ["Japanese Shino glaze", "183, 186"],
                    ["Japanese tea ceremony", "183  "],

                    ["Kaki glaze", "61,158 "],
                    ["kaolin", "7, 8 "],
                    ["kiln setting clay", "17 "],
                    ["kiln wadding", "17"],
                    ["KNaO", "5, 44"],
                    ["Kuan glaze", "57, 140, 179"],

                    ["labelling", "24 "],
                    ["lime/alkali balance in iron glazes", "164"],
                    ["lime/alkali glazes", "43 "],
                    ["lime in glazes", "43 "],
                    ["limits", "xii "],
                    ["line blend", "20 "],
                    ["liquidus line", "84 "],
                    ["liquidus plane", "90 "],
                    ["lizard skin glaze", "65"],

                    ["machine aesthetic", "183 "],
                    ["magnesia, effect in copper red glazes", "191 "],
                    ["magnesia, role in iron glazes", "164"],
                    ["magnesia, sources of", "62 "],
                    ["magnesium carbonate", "7, 62 "],
                    ["magnesium glazes", "62 "],
                    ["magnesite", "7, 62 "],
                    ["marbled Shino glaze", "184 "],
                    ["materials", "xii "],
                    ["matt glazes", "37, 134 "],
                    ["methodology", "xii, 120 "],
                    ["molecular parts", "15 "],
                    ["molecules", "11 "],
                    ["M.P.", "15"],
                    ["N nepheline syenite", "5 "],
                    ["nepheline syenite Shino", "185, 186"],
                    ["nickel reds and blues", "129, 132"],
                    ["nucleation", "125"],
                    ["numbering system for glazes", "47"],


                    ["oatmeal glaze", "65 "],
                    ["oilspot tenmoku glaze", "166 "],
                    ["Ogama", "184, 185 "],
                    ["opacifiers", "141 "],
                    ["opaque glazes", "141, 156 "],
                    ["orangepeel effect", "37 "],
                    ["order of calculation", "92, 108 "],
                    ["Oribe ware", "183 "],
                    ["oxides", "12 "],
                    ["oxide weight charts", "45 "],
                    ["oxide weight percentage", "13 "],
                    ["oxy probe", "47"],

                    ["partial blends", "115 "],
                    ["parts chart", "30 "],
                    ["parts chart calculations", "111 "],
                    ["peach bloom glaze", "190, 192"],
                    ["percentage calculation", "94, 99"],
                    ["percentage method", "107 "],
                    ["phase equilibria diagrams", "84"],
                    ["pigments", "153 "],
                    ["pigments, recipes of", "154 "],
                    ["pigskin effect", "65 "],
                    ["pink matt glaze", "35, 37 "],
                    ["preparation of glazes", "xii "],
                    ["pyroxene crystals", "62, 128, 131, 163, 168"],


                    ["Queensland Potters' Association", "ix"],

                    ["raw materials", "4 "],
                    ["recipe", "13 "],
                    ["recipe charts", "45 "],
                    ["recording data", "24 "],
                    ["red Shino glaze", "184 "],
                    ["results", "xiii "],
                    ["results charts", "45 "],
                    ["RO", "12 "],
                    ["rock dust", "21,204 "],
                    ["rust break (in iron glazes)", "165"],
                    ["rust glaze", "158, 159, 164"],

                    ["salt", "44 "],
                    ["salt in Shino glazes", "185, 186, 187"],
                    ["sang-de-boeuf glaze", "189, 192"],
                    ["Seger formula", "13"],
                    ["seeding of crystals (artificial)", "128"],
                    ["Shigaraki clay and firing", "194, 195"],
                    ["Shino glaze", "183 "],
                    ["shiny glazes", "37 "],
                    ["silica", "36 "],
                    ["silica, colloidal", "146 "],
                    ["silica matt glazes", "53, 65,139 "],
                    ["silicon carbide", "154, 191 "],
                    ["simultaneous equations", "104 "],
                    ["slips", "150, 151 "],
                    ["slips, coloured", "153 "],
                    ["slips, recipes of", "152 "],
                    ["slips, trouble-shooting of", "152"],
                    ["starting points", "25"],
                    ["striking", "189, 192 "],
                    ["stringing", "37, 49, 53 "],
                    ["sugary glazes", "38 "],
                    ["supercooled liquid", "124 "],
                    ["suspender", "181"],

                    ["talc", "7, 62 "],
                    ["teadust glaze", "158, 159, 162, 163, 164, 165, 168 "],
                    ["teadust effect", "168 "],
                    ["tenmoku", "158, 165, 170, 171 "],
                    ["tenmoku, oilspot", "166 "],
                    ["tessha glaze", "61, 158, 169, 170"],
                    ["test firings", "121"],
                    ["tin oxide, effect on copper red glazes", "191"],
                    ["titanite crystals", "128 "],
                    ["tomato red glaze", "169 "],
                    ["trial and error (calculation)", "104"],
                    ["triaxial diagrams", "87, 114 "],
                    ["turquoise copper glaze", "188"],

                    ["unity formula", "94 "],
                    ["unity formula for iron glazes", "158"],

                    ["vaporisation of fluxes", "39 "],
                    ["vapour imprint diagrams", "39 "],
                    ["volumetric blending, biaxial", "28, 29"],
                    ["volumetric blending, line", "21, 23"],


                    ["white tenmoku", "183 "],
                    ["whiteware", "150 "],
                    ["whiting", "7, 15, 43 "],
                    ["woodash", "20 "],
                    ["woodash analyses", "199"],


                    ["yellow Seto glaze", "177, 183"],

                    ["zinc crystal glazes", "128, 130 "],
                    ["zinc glazes", "68 "],
                    ["zinc oxide, sources of", "68 "],
                    ["zinc oxide, vaporisation of", "39, 71"],

                    
                    
                ]
        seq=1
        for i in items:
            seq=seq+1
            #logging.debug("attempting: " + i[0])
            item= IndexItem()
            item.label=i[0]
            item.pageNumbers=i[1].upper()
            item.sequenceNumber=seq
            item.put()
        response = redirect_to('admin-index')
        response.data = ''
        return response

