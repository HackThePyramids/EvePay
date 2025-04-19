from flask import *
from preston import Preston
import webbrowser
import time
import threading

contractor = Preston()
started = False
contracts= [216975583]
app = Flask(__name__)
preston = Preston(user_agent='eve-stop',
                  client_id='ddb2dd16e76a44cc99f8049b4f4306c4',
                  client_secret='JqMW0Dt8yrUYKWI6zVCCC0BkcVSQUvetO5A6eOVn',
                  callback_url='http://localhost/callback',
                  scope= 'publicData esi-calendar.respond_calendar_events.v1 esi-calendar.read_calendar_events.v1 esi-location.read_location.v1 esi-location.read_ship_type.v1 esi-mail.organize_mail.v1 esi-mail.read_mail.v1 esi-mail.send_mail.v1 esi-skills.read_skills.v1 esi-skills.read_skillqueue.v1 esi-wallet.read_character_wallet.v1 esi-wallet.read_corporation_wallet.v1 esi-search.search_structures.v1 esi-clones.read_clones.v1 esi-characters.read_contacts.v1 esi-universe.read_structures.v1 esi-killmails.read_killmails.v1 esi-corporations.read_corporation_membership.v1 esi-assets.read_assets.v1 esi-planets.manage_planets.v1 esi-fleets.read_fleet.v1 esi-fleets.write_fleet.v1 esi-ui.open_window.v1 esi-ui.write_waypoint.v1 esi-characters.write_contacts.v1 esi-fittings.read_fittings.v1 esi-fittings.write_fittings.v1 esi-markets.structure_markets.v1 esi-corporations.read_structures.v1 esi-characters.read_loyalty.v1 esi-characters.read_chat_channels.v1 esi-characters.read_medals.v1 esi-characters.read_standings.v1 esi-characters.read_agents_research.v1 esi-industry.read_character_jobs.v1 esi-markets.read_character_orders.v1 esi-characters.read_blueprints.v1 esi-characters.read_corporation_roles.v1 esi-location.read_online.v1 esi-contracts.read_character_contracts.v1 esi-clones.read_implants.v1 esi-characters.read_fatigue.v1 esi-killmails.read_corporation_killmails.v1 esi-corporations.track_members.v1 esi-wallet.read_corporation_wallets.v1 esi-characters.read_notifications.v1 esi-corporations.read_divisions.v1 esi-corporations.read_contacts.v1 esi-assets.read_corporation_assets.v1 esi-corporations.read_titles.v1 esi-corporations.read_blueprints.v1 esi-contracts.read_corporation_contracts.v1 esi-corporations.read_standings.v1 esi-corporations.read_starbases.v1 esi-industry.read_corporation_jobs.v1 esi-markets.read_corporation_orders.v1 esi-corporations.read_container_logs.v1 esi-industry.read_character_mining.v1 esi-industry.read_corporation_mining.v1 esi-planets.read_customs_offices.v1 esi-corporations.read_facilities.v1 esi-corporations.read_medals.v1 esi-characters.read_titles.v1 esi-alliances.read_contacts.v1 esi-characters.read_fw_stats.v1 esi-corporations.read_fw_stats.v1 esi-characterstats.read.v1')


def payment_watcher(contractor):
    while True:
        global contract_status
        contract_status = contractor.get_op("get_characters_character_id_contracts", character_id=2121086215)
        print(contract_status)
        time.sleep(300)
def isPaid(id):
    result = next((p for p in contract_status if p['contract_id'] == id), None)
    if result["status"] == "finished":
        return "True"
    else:
        return "False"



@app.route('/pay')
def index():
    return render_template(
        "index.html",
        url=preston.get_authorize_url()
    )
@app.route('/check_payment_status')
def check_payment_status():
    id = request.args.get("payment_id")
    return isPaid(id)


@app.route("/payment_success")
def payment_success():
    return "Yay you done paid it"
    
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        auth = preston.authenticate(code)
        if auth.whoami()["CharacterName"] == "Hurvel Darmazaf":
            
            watcher_thread = threading.Thread(target=payment_watcher, args=(auth,))
            watcher_thread.daemon = True
            watcher_thread.start()
            return "okidoki auth successful"
            
        else:
            ctopay = contracts[0]
            auth.post_op("post_ui_openwindow_contract", post_data={"contract_id": ctopay}, path_data=[])
            return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Waiting for Payment</title>
        <script>
        function checkPayment() {
            fetch('/check_payment_status?payment_id={{ payment_id }}')
                .then(response => response.text())
                .then(text => {
                    if (text === 'True') {
                        window.location.href = '/payment_success';
                    } else {
                        setTimeout(checkPayment, 2000);
                    }
                });
        }

        window.onload = checkPayment;
        </script>
    </head>
    <body>
        <h1>Waiting for your payment...</h1>
    </body>
    </html>
    ''', payment_id=ctopay)



        
        # Proceed with authenticated ESI calls
        
        

    else:
        return 'No code found in the callback.', 400


if __name__ == '__main__':
   
      # <- important so it stops when you stop Flask
    
    app.run(port=80)

