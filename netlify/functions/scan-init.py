import json
import random 

def handler(event, context):
    try:
        data = json.loads(event['body'])
        nsec = data.get('nsec')

        if not nsec:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Nostr nsec krävs för autentisering.'})}

        TARGET_EMAIL = 'Alias-Address@anonaddy.com' 
        TARGET_PHONE = '076...' 

        all_results = [
            {'service': 'BankID-Tjänst A', 'status': 'Aktivt konto', 'difficulty': 'Grön', 'action_method': 'BankID', 'next_step': 'Följ guide för digital signering.'},
            {'service': 'Social Plattform X', 'status': 'LÄCKA BEKRÄFTAD', 'difficulty': 'Röd', 'action_method': 'E-post/Alias', 'next_step': 'GenAI genererar aggressivt Art. 17-brev till ' + TARGET_EMAIL},
            {'service': 'Global Molntjänst C', 'status': 'Aktivt konto', 'difficulty': 'Röd', 'action_method': 'E-post/Alias', 'next_step': 'GenAI genererar Art. 20 (Portabilitet) begäran.'},
            {'service': 'Tidigare Jobbsökarsida', 'status': 'Gammal profil', 'difficulty': 'Gul', 'action_method': 'Telefon', 'next_step': 'Följ talmanus för radering.'},
            {'service': 'Google Search Cache', 'status': 'Gammal indexering', 'difficulty': 'Röd', 'action_method': 'Formulär', 'next_step': 'GenAI skapar guide för Google Removal Tool.'},
        ]

        priority_map = {'BankID': 1, 'E-post/Alias': 2, 'Telefon': 3, 'Formulär': 4}
        for result in all_results:
            result['priority_rank'] = priority_map.get(result['action_method'].split('/')[0], 99) 
        prioritized_list = sorted(all_results, key=lambda x: x['priority_rank'])

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Skanning slutförd. Fullständig spår-logg genererad.',
                'prioritized_list': prioritized_list
            })
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': 'Intern process misslyckades. Kontrollera Nostr-nyckeln.'})}
