FORBIDDEN_FIELDS = {'pk': 'tt_id',
                    'ok': 'tt_orig_id',
                    'cu': 'tt_create_modif_user_id',
                    'du': 'tt_delete_user_id',
                    'vf': 'tt_valid_from_ts',
                    'vu': 'tt_valid_until_ts'}

PK = FORBIDDEN_FIELDS.get('pk')
OK = FORBIDDEN_FIELDS.get('ok')
CU = FORBIDDEN_FIELDS.get('cu')
DU = FORBIDDEN_FIELDS.get('du')
VF = FORBIDDEN_FIELDS.get('vf')
VU = FORBIDDEN_FIELDS.get('vu')

MAX = 999999999999
