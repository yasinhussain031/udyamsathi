import os, math
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/googlef2125f80e8d4bfb0.html')
def google_verification():
    return send_from_directory('.', 'googlef2125f80e8d4bfb0.html')


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')

BUSINESSES = {
    'Dairy & Milk Products': {
        'capital': 150000, 'revenue': 65000, 'margin': 18, 'growth': 72, 'demand': 82, 'jobs': 3,
        'opportunity': 'Daily local demand can be expanded through paneer, curd, ghee and doorstep delivery.',
        'strengths': ['Recurring daily demand', 'Multiple value-added products', 'Local sourcing can reduce transport dependence', 'Repeat-customer potential'],
        'weaknesses': ['Perishable inventory', 'Feed and input costs can compress margins', 'Cold storage and hygiene require attention', 'Daily operations are labour intensive'],
        'opportunities': ['Paneer/curd/ghee value addition', 'Household delivery subscriptions', 'Hotel, canteen and tea-shop supply', 'FPO/SHG-linked local branding'],
        'threats': ['Feed price increases', 'Milk price fluctuations', 'Spoilage and quality failures', 'Dependence on a small buyer network'],
        'risks': [('Feed/input inflation', 'Compare suppliers, formulate a monthly input budget and keep a working-capital reserve.'), ('Spoilage', 'Use batch-level inventory discipline, cold storage where needed and daily sales planning.'), ('Buyer concentration', 'Build household, retail and institutional channels instead of relying on one buyer.')],
        'channels': ['Households', 'Tea shops', 'Hotels/canteens', 'Weekly market', 'Home delivery'],
        'pricing': 'Track local prices weekly and use tiered packs. Price value-added products separately so packaging and delivery costs are recovered.',
        'validation': 'Can you secure recurring household or institutional demand before investing in additional animals/equipment?'
    },
    'Tailoring & Garments': {
        'capital': 90000, 'revenue': 45000, 'margin': 32, 'growth': 78, 'demand': 79, 'jobs': 2,
        'opportunity': 'Low entry cost with scope for school uniforms, alterations, blouse stitching and local orders.',
        'strengths': ['Low starting capital', 'High service margin potential', 'Can operate from home', 'Flexible product mix'],
        'weaknesses': ['Skill dependent', 'Capacity limited by working hours', 'Seasonal order peaks', 'Customer acquisition may start slowly'],
        'opportunities': ['School uniforms', 'Women-focused tailoring', 'SHG/community orders', 'WhatsApp/local digital orders'],
        'threats': ['Low-price competitors', 'Ready-made clothing', 'Demand dips outside seasons', 'Fabric price changes'],
        'risks': [('Competition', 'Differentiate through fitting, turnaround time, customization and reliable delivery.'), ('Seasonality', 'Balance festive/school orders with alterations and recurring stitching services.'), ('Skill bottleneck', 'Standardize common designs and train an additional helper before scaling.')],
        'channels': ['Walk-in customers', 'Schools', 'SHGs', 'Local boutiques', 'WhatsApp orders'],
        'pricing': 'Separate labour, material and urgent-order charges. Offer bundled school-uniform or family packages while protecting labour margin.',
        'validation': 'Can you collect enough paid trial orders from nearby households, schools or groups to fill at least 50% of initial capacity?'
    },
    'Food Processing': {
        'capital': 250000, 'revenue': 110000, 'margin': 24, 'growth': 82, 'demand': 84,
        'opportunity': 'Value-add local crops into packaged products with better shelf life and wider distribution.',
        'strengths': ['Value addition can improve unit economics', 'Can use local agricultural output', 'Scalable product range', 'Longer shelf-life options than raw produce'],
        'weaknesses': ['Higher equipment requirement', 'Packaging/compliance costs', 'Brand building takes time', 'Quality consistency is critical'],
        'opportunities': ['Pickles/spices/flours', 'Local crop-based products', 'Retail and institutional supply', 'FPO/SHG and district-level distribution'],
        'threats': ['Raw material price swings', 'Quality or compliance failures', 'Established packaged brands', 'Slow-moving inventory'],
        'risks': [('Raw material volatility', 'Map crop seasons, compare suppliers and contract only after demand is validated.'), ('Compliance', 'Verify current food-registration, labelling and packaging requirements before commercial launch.'), ('Unsold inventory', 'Start with small batches and use pre-orders/retailer commitments to control stock.')],
        'channels': ['Village retail', 'District retailers', 'FPO/SHG networks', 'Local delivery', 'Institutional buyers'],
        'pricing': 'Use cost-plus pricing with separate packaging, transport and retailer margin allowances. Test 2–3 pack sizes and monitor repeat purchase.',
        'validation': 'Which local crop/raw material and product format can you source consistently while getting retailers to accept a repeat order?'
    },
    'Poultry': {
        'capital': 180000, 'revenue': 90000, 'margin': 20, 'growth': 68, 'demand': 78,
        'opportunity': 'Regular demand is possible when biosecurity, batch planning and buyer relationships are strong.',
        'strengths': ['Frequent demand cycle', 'Can scale in batches', 'Local buyer network possible', 'Short production cycles can provide learning quickly'],
        'weaknesses': ['Disease can create large losses', 'Feed is a major cost', 'Requires daily monitoring', 'Market prices can move quickly'],
        'opportunities': ['Direct local sales', 'Contract/institutional buyers', 'Improved feed and batch planning', 'Value-added/cleaned supply where permitted'],
        'threats': ['Disease outbreaks', 'Feed inflation', 'Wholesale price drops', 'Buyer concentration'],
        'risks': [('Disease', 'Follow biosecurity, vaccination and veterinary guidance; isolate risk where possible.'), ('Feed inflation', 'Compare suppliers, track feed conversion and avoid overstocking.'), ('Price swings', 'Pre-identify multiple buyers and plan batch sizes around expected demand.')],
        'channels': ['Households', 'Retail meat shops', 'Hotels', 'Wholesale buyers'],
        'pricing': 'Track local selling prices and calculate a minimum acceptable margin per bird/batch before increasing capacity.',
        'validation': 'Can you identify at least 2–3 reliable buyers and estimate a selling price before placing the first major batch order?'
    },
    'Agri-input Store': {
        'capital': 300000, 'revenue': 125000, 'margin': 16, 'growth': 76, 'demand': 83,
        'opportunity': 'Strong fit near farming clusters where crop-linked input demand is concentrated.',
        'strengths': ['Repeat farmer customers', 'Crop-cycle demand', 'Cross-selling potential', 'Location near farms can reduce customer acquisition cost'],
        'weaknesses': ['Higher inventory requirement', 'Working capital can get locked', 'Credit sales can create cash-flow pressure', 'Licensing/product rules may apply'],
        'opportunities': ['Crop-specific input bundles', 'Advisory + input packs', 'Farmer delivery service', 'FPO-linked procurement'],
        'threats': ['Seasonal demand swings', 'Credit defaults', 'Large dealer competition', 'Product price changes'],
        'risks': [('Inventory lock-in', 'Stock around crop calendars and reorder based on actual movement, not assumptions.'), ('Credit risk', 'Set clear credit limits and prefer cash/digital payment for new customers.'), ('Regulatory/product rules', 'Verify applicable licences, authorised products and current government rules before stocking.')],
        'channels': ['Farmers', 'FPOs', 'SHGs', 'Local agricultural clusters', 'Farm delivery'],
        'pricing': 'Maintain transparent category-wise margins and avoid excessive credit exposure. Use crop-season bundles to increase basket size.',
        'validation': 'Can you map nearby crop clusters and identify the top 20 input products customers repeatedly purchase before stocking inventory?'
    },
    'Grocery / Kirana': {
        'capital': 200000, 'revenue': 100000, 'margin': 14, 'growth': 65, 'demand': 88,
        'opportunity': 'Stable recurring demand can be strengthened with home delivery and digital ordering.',
        'strengths': ['Essential products', 'Frequent repeat purchases', 'Simple customer discovery', 'Can start with fast-moving SKUs'],
        'weaknesses': ['Thin average margins', 'Inventory management is critical', 'Price competition', 'Cash can be tied in slow-moving stock'],
        'opportunities': ['Home delivery', 'Monthly family packs', 'Local digital ordering', 'Institutional supply to small eateries/hostels'],
        'threats': ['Supermarkets/e-commerce', 'Supplier price changes', 'Customer credit risk', 'Expiry/slow-moving stock'],
        'risks': [('Thin margins', 'Focus on fast-moving products, supplier comparison and controlled discounting.'), ('Inventory', 'Use a reorder list and remove slow-moving SKUs before they consume working capital.'), ('Credit', 'Set customer credit limits and prefer digital/cash settlement.')],
        'channels': ['Households', 'Schools/hostels', 'Small eateries', 'Home delivery', 'WhatsApp ordering'],
        'pricing': 'Protect margins with fast-moving SKUs, supplier comparison and small convenience bundles rather than blanket discounting.',
        'validation': 'How many households can you realistically serve within your delivery/walk-in radius, and what are their top recurring purchases?'
    },
    'Rural Homestay': {
        'capital': 450000, 'revenue': 85000, 'margin': 28, 'growth': 80, 'demand': 70,
        'opportunity': 'Potentially attractive where attractions, road access and visitor flow support stays.',
        'strengths': ['Higher value per customer', 'Can combine food/local experiences', 'Uses existing property where available', 'Differentiation through local culture'],
        'weaknesses': ['Seasonal demand', 'Service quality matters', 'Higher setup cost', 'Reviews/reputation take time'],
        'opportunities': ['Farm experiences', 'Local cuisine packages', 'Weekend/staycation offers', 'Tie-ups with local attractions'],
        'threats': ['Low tourist footfall', 'Platform dependence', 'Local permissions/standards', 'Unexpected maintenance costs'],
        'risks': [('Low footfall', 'Validate visitor flow, attractions and competitor occupancy before renovation.'), ('Platform dependence', 'Build direct booking channels and local partnerships.'), ('Permissions', 'Confirm applicable local registration, safety and tourism requirements before launch.')],
        'channels': ['Direct bookings', 'Travel platforms', 'Local tourism networks', 'Social media', 'Travel agents'],
        'pricing': 'Use weekday/weekend pricing and package room + meal + local experience instead of selling only a room.',
        'validation': 'What nearby attraction or recurring visitor segment can generate enough occupancy outside peak weekends?'
    }
}

LOCATION_PROFILES = {
    'Nashik, Maharashtra': {'population':145000,'market':86,'farm':72,'tourism':60,'road':82,'note':'Strong mix of farming, food activity and urban-rural connectivity.','crop':'Grapes, onion and vegetables'},
    'Pune Rural, Maharashtra': {'population':180000,'market':91,'farm':55,'tourism':72,'road':91,'note':'Large nearby consumer base with strong connectivity and service demand.','crop':'Vegetables, dairy and horticulture'},
    'Ahmednagar, Maharashtra': {'population':120000,'market':78,'farm':80,'tourism':48,'road':76,'note':'Agriculture-linked demand can support farm, food and retail businesses.','crop':'Onion, sugarcane and grains'},
    'Satara, Maharashtra': {'population':95000,'market':76,'farm':74,'tourism':68,'road':78,'note':'Agriculture and tourism create mixed local opportunities.','crop':'Sugarcane, vegetables and horticulture'},
    'Kolhapur, Maharashtra': {'population':135000,'market':84,'farm':76,'tourism':62,'road':84,'note':'Strong local consumption and agricultural ecosystem.','crop':'Sugarcane, dairy and vegetables'},
    'Nagpur Rural, Maharashtra': {'population':155000,'market':82,'farm':67,'tourism':50,'road':86,'note':'Large regional market with good transport connectivity.','crop':'Orange, soybean and grains'},
    'Chhatrapati Sambhajinagar, Maharashtra': {'population':145000,'market':83,'farm':64,'tourism':77,'road':83,'note':'Manufacturing, tourism and surrounding rural demand provide varied opportunities.','crop':'Cotton, soybean and horticulture'},
    'Other / Enter manually': {'population':100000,'market':70,'farm':60,'tourism':50,'road':70,'note':'Generic prototype profile; production version should use live locality data.','crop':'Local crop data to be fetched'}
}

INCOME_OPTIONS={'under_100000':75000,'100000_250000':175000,'250000_500000':375000,'500000_1000000':750000,'above_1000000':1250000}
MARGIN_OPTIONS={'25000':25000,'50000':50000,'75000':75000,'100000':100000,'150000':150000,'250000':250000,'500000':500000,'1000000':1000000}


def money(v): return round(float(v or 0))

def emi(principal, annual_rate, months):
    if principal <= 0 or months <= 0: return 0
    r=annual_rate/12/100
    return principal/months if r==0 else principal*r*(1+r)**months/((1+r)**months-1)

def scheme_for(project):
    if project<=140000: return {'name':'Micro Finance Scheme','rate':6.5,'months':36,'moratorium':3,'max_loan':125000,'tier':'micro'}
    if project<=5000000: return {'name':'Term Loan Scheme','rate':8.0,'months':84,'moratorium':6,'max_loan':4500000,'tier':'term'}
    return None

def finance(margin):
    project=margin/0.10; scheme=scheme_for(project)
    if not scheme:
        return {'margin':margin,'project':project,'loan':None,'scheme':'Outside the specified PS financing tiers','warning':'The prototype models the two configured financing tiers.'}
    requested=project*.90; loan=min(requested,scheme['max_loan']); monthly=emi(loan,scheme['rate'],scheme['months'])
    total=monthly*scheme['months']
    return {'margin':margin,'project':project,'requested_loan':requested,'loan':loan,'scheme':scheme['name'],'rate':scheme['rate'],'months':scheme['months'],'moratorium':scheme['moratorium'],'emi':monthly,'quarterly':monthly*3,'total_repayment':total,'interest_estimate':max(0,total-loan),'cap_warning':requested>scheme['max_loan'],'tier':scheme['tier']}

def profile(location): return LOCATION_PROFILES.get(location, LOCATION_PROFILES['Other / Enter manually'])

def recommendations(margin, location, income):
    lp=profile(location); rows=[]
    for name,b in BUSINESSES.items():
        capital_fit=max(0,100-abs(margin-b['capital'])/max(b['capital'],1)*45)
        affordability=100 if margin>=b['capital']*.10 else max(35,margin/(b['capital']*.10)*100)
        local_bonus=0
        if name in ['Dairy & Milk Products','Food Processing','Poultry','Agri-input Store']: local_bonus+=lp['farm']*.12
        if name=='Rural Homestay': local_bonus+=lp['tourism']*.18
        if name in ['Tailoring & Garments','Grocery / Kirana']: local_bonus+=lp['market']*.10
        score=capital_fit*.40+affordability*.20+b['growth']*.18+b['demand']*.12+local_bonus*.10
        rows.append((score,name,b))
    rows.sort(reverse=True)
    return [{'name':n,'capital':b['capital'],'revenue':b['revenue'],'score':round(s,1),'opportunity':b['opportunity']} for s,n,b in rows[:4]]

def build_analysis(location, margin, income, category=None):
    lp=profile(location)
    if category in BUSINESSES: selected=category; suggested=False
    else: selected=recommendations(margin,location,income)[0]['name']; suggested=True
    b=BUSINESSES[selected]; fin=finance(margin)
    affordability=max(35,min(100,(margin/max(b['capital']*.10,1))*100))
    fit=round(max(45,min(97, b['demand']*.35+b['growth']*.20+lp['market']*.18+lp['road']*.07+affordability*.20)))
    market=round(max(45,min(97,lp['market']*.55+b['demand']*.25+lp['road']*.10+lp['farm']*.10)))
    reachable=round(lp['population']*(.035+market/5000)); customers=round(reachable*(.10+b['demand']/1000))
    monthly=b['revenue']*(.88+market/300); annual=monthly*12; op_profit=annual*b['margin']/100
    fixed=max(6000,monthly*.18); break_even=fixed/max(b['margin']/100,.05)
    working=b['capital']*.20; income_ratio=margin/max(income,1)
    feasibility='Strong' if fit>=80 and market>=80 else 'Promising' if fit>=68 and market>=65 else 'Needs validation'
    capital_gap=max(0,b['capital']-fin['project'])
    summary=(f'{selected} is a {feasibility.lower()} prototype fit for {location}. The model estimates an indicative 5–10 km serviceable catchment of about {customers:,} potential customer units. Your available margin of ₹{money(margin):,} maps to an indicative project cost of ₹{money(fin["project"]):,} under the 10% margin formula, subject to scheme caps and eligibility.')
    actions=[
        f'Validate demand with 20–30 local customer conversations and at least 5 paid/committed trial orders.',
        f'Compare at least 3 suppliers and record landed cost, transport, payment terms and minimum order size.',
        f'Reserve approximately ₹{money(working):,} as working-capital buffer in the prototype capital plan.',
        f'Run a small pilot before full investment; target repeat demand and track unit economics weekly.',
        'Verify current government scheme eligibility, documents, contribution, registration and repayment terms on official portals.'
    ]
    if selected=='Food Processing': actions[0]='Validate crop/raw-material seasonality, local retailer interest and repeat purchase before buying major equipment.'
    if selected=='Rural Homestay': actions[0]='Validate visitor footfall, nearby attractions, road access and competing stay prices before renovation.'
    if selected=='Agri-input Store': actions[0]='Map nearby crop clusters and seasonal input demand; identify the top 20 products before stocking inventory.'
    return {
      'location':location,'selected':selected,'suggested':suggested,'business':b,'location_profile':lp,'fit':fit,'market':market,'feasibility_label':feasibility,
      'finance_label':'Comfortable' if income_ratio<=.35 else 'Moderate' if income_ratio<=.60 else 'High capital commitment','recommendations':recommendations(margin,location,income),'finance':fin,
      'market_analysis':{'catchment':'Indicative 5–10 km','reachable_population':reachable,'primary_customers':customers,'distribution':b['channels'],'local_market_index':lp['market'],'road_access':lp['road'],'agri_index':lp['farm'],'tourism_index':lp['tourism']},
      'feasibility_report':{
        'executive':summary,
        'local_context':lp['note'],
        'demand_case':f"The business demand signal is {b['demand']}/100. The local market index is {lp['market']}/100, while road access is {lp['road']}/100. These are prototype indicators, not measured market facts.",
        'customer_segments':[f'Households and consumers within the indicative catchment', 'Small retailers/service buyers', 'Institutional buyers where relevant', 'Repeat customers generated through delivery/community channels'],
        'distribution_logic':f"Recommended channels are prioritised around {', '.join(b['channels'][:3])}. Start with the lowest-cost channel, measure conversion and then add distribution layers.",
        'local_crop':lp['crop'],
        'capital_fit':f"Reference business setup cost in the prototype is ₹{money(b['capital']):,}. Your indicative project capacity is ₹{money(fin['project']):,}. {'There is a prototype funding gap of ₹'+format(money(capital_gap),',')+' versus this reference setup.' if capital_gap else 'Your indicative project capacity covers the reference setup cost.'}",
        'decision': 'Proceed to validation' if fit>=75 and market>=70 else 'Validate before investment'
      },
      'financial_analysis':{
        'estimated_monthly_revenue':monthly,'estimated_annual_revenue':annual,'estimated_annual_operating_margin':op_profit,'monthly_fixed_cost_proxy':fixed,'break_even_monthly_sales':break_even,'income_to_margin_ratio':income_ratio,
        'capital_plan':{'equipment':b['capital']*.42,'inventory':b['capital']*.23,'setup':b['capital']*.15,'working_capital':working},
        'unit_economics':{'gross_margin_proxy':b['margin'],'jobs':b.get('jobs', 1),'reference_capital':b['capital']},
        'growth':[annual,annual*1.15,annual*1.32]
      },
      'swot':{'strengths':b['strengths'],'weaknesses':b['weaknesses'],'opportunities':b['opportunities'],'threats':b['threats']},
      'risk_plan':[{'risk':r,'mitigation':m} for r,m in b['risks']], 'pricing':b['pricing'],'validation_question':b['validation'],'action_plan':actions,
      'scheme_router':{'why':f"The prototype routes the indicative project cost of ₹{money(fin['project']):,} to {fin['scheme']}. This follows the configured financing thresholds.", 'eligibility':['Confirm beneficiary/category eligibility with the implementing agency','Confirm current project-cost and loan ceilings','Prepare identity/address/income/business documents as required','Verify current contribution, interest, moratorium and repayment conditions','Use official portals/agency guidance before applying']},
      'note':'Prototype intelligence only. Market population, customer counts, revenue and growth values are illustrative model outputs. Production must replace demo profiles with verified Government/open data and current scheme rules.'
    }

@app.route('/')
def home():
    return render_template('index.html', businesses=list(BUSINESSES), locations=list(LOCATION_PROFILES))

@app.post('/api/analyze')
def analyze():
    data=request.get_json(force=True)
    location=(data.get('location') or 'Other / Enter manually').strip()
    if location=='Other / Enter manually': location=(data.get('custom_location') or '').strip() or location
    income_key=str(data.get('income') or '')
    margin_key=str(data.get('margin') or '')
    income=INCOME_OPTIONS.get(income_key)
    margin=MARGIN_OPTIONS.get(margin_key)
    if income is None:
        try: income=float(data.get('custom_income'))
        except: income=0
    if margin is None:
        try: margin=float(data.get('custom_margin'))
        except: margin=0
    category=(data.get('category') or '').strip()
    if category=='Other / Enter manually': category=(data.get('custom_category') or '').strip()
    if margin<=0: return jsonify({'error':'Enter a valid available margin capital.'}),400
    if income<=0: return jsonify({'error':'Enter a valid annual income.'}),400
    return jsonify(build_analysis(location,margin,income,category))

@app.post('/api/chat')
def chat():
    p=request.get_json(force=True); q=(p.get('message') or '').lower(); lang=p.get('lang','en')
    if any(x in q for x in ['margin','capital','project cost']): ans='Available margin ÷ 10% gives the indicative project cost. Example: ₹1 lakh margin → ₹10 lakh project cost → up to 90% loan component, subject to the scheme cap and eligibility.'
    elif 'emi' in q: ans='The prototype calculates an indicative EMI using the applicable financing tier. Actual moratorium and repayment treatment must be confirmed with the official channelizing agency/lender.'
    elif 'scheme' in q or 'loan' in q: ans='The prototype routes projects up to ₹1.40 lakh to the Micro Finance tier and projects above ₹1.40 lakh up to ₹50 lakh to the Term Loan tier, using the configured financing parameters.'
    elif 'swot' in q: ans='SWOT is business-specific: strengths and weaknesses describe internal conditions; opportunities and threats describe external factors. UdyamSathi also pairs major threats with practical mitigations.'
    elif 'feasibility' in q or 'market' in q: ans='The report combines indicative catchment, customer estimate, local market signals, channels, product-market fit, pricing, growth and risk. In production, verified local datasets should replace demo profiles.'
    elif 'registration' in q or 'udyam' in q: ans='Use the official Udyam Registration portal for MSME registration and verify current requirements before applying.'
    else: ans='I can explain feasibility, SWOT, project cost, schemes, EMI, market reach, pricing, risks, registration and the 90-day action plan. Try “explain my financing” or “how is SWOT calculated?”'
    localized={'hi':'मैं व्यवहार्यता, SWOT, प्रोजेक्ट लागत, ऋण, EMI, बाजार, मूल्य निर्धारण और पंजीकरण समझा सकता हूँ।','mr':'मी व्यवहार्यता, SWOT, प्रकल्प खर्च, कर्ज, EMI, बाजार आणि नोंदणी समजावू शकतो.','ta':'சாத்தியம், SWOT, திட்டச் செலவு, கடன், EMI, சந்தை மற்றும் பதிவை விளக்க முடியும்.','te':'సాధ్యత, SWOT, ప్రాజెక్ట్ ఖర్చు, రుణం, EMI, మార్కెట్ మరియు రిజిస్ట్రేషన్ వివరించగలను.','bn':'আমি সম্ভাব্যতা, SWOT, প্রকল্প খরচ, ঋণ, EMI, বাজার এবং নিবন্ধন ব্যাখ্যা করতে পারি.'}
    if lang!='en' and not any(x in q for x in ['margin','capital','project','emi','scheme','loan','swot','feasibility','market','registration','udyam']): ans=localized.get(lang,ans)
    return jsonify({'answer':ans})

if __name__=='__main__':
    app.run(host='127.0.0.1',port=int(os.getenv('PORT','5000')),debug=True)
