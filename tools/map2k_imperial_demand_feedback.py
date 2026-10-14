"""Runtime schema and refusal feedback fixes; no free declarations of war."""
import re
import validate_diplomacy_ottoman_1776 as cw
from map2a_patch import edits
from map2k_imperial_feedback import block,child,EF,EV,WG,DP

def augment_demand_feedback(files):
 loc={}
 def L(k,en,fr):loc[k]=(en,fr)
 # Native generic diplomatic responses do not reuse country-event .t/.d.
 for key,label,frlabel in [
  ('aor1776_hre_request_subject_release','imperial liberation','libération impériale'),
  ('aor1776_hre_request_restitution','imperial restitution','rétrocession impériale'),
  ('aor1776_hre_enforce_internal_restitution','imperial restitution','rétrocession impériale')]:
  L(key+'_proposal_notification_name','Imperial summons — '+label,'Sommation impériale — '+frlabel)
  if 'subject_release' in key:
   L(key+'_proposal_notification_desc',"[INITIATOR_COUNTRY.GetName] demands the release of our imperial subjects listed below and the restoration of their registered territorial rights. This diplomatic request covers the listed estates collectively. A separately launched liberation play targets one selected estate; further war goals must be added deliberately.","[INITIATOR_COUNTRY.GetName] exige la libération de nos sujets impériaux listés ci-dessous et le rétablissement de leurs droits territoriaux enregistrés. Cette demande diplomatique porte collectivement sur les États listés. Un coup diplomatique de libération lancé séparément vise un seul État sélectionné ; les autres objectifs doivent être ajoutés volontairement.")
  else:
   L(key+'_proposal_notification_desc',"[INITIATOR_COUNTRY.GetName] demands that the imperial provinces listed below be restored to their registered legitimate holders. Review the territories and the consequences of accepting or refusing before answering.","[INITIATOR_COUNTRY.GetName] exige que les provinces impériales listées ci-dessous soient rendues à leurs titulaires légitimes enregistrés. Examinez les territoires et les conséquences d’un accord ou d’un refus avant de répondre.")
  for response,en,fr in [('accepted','accepted','accepté'),('declined','refused','refusé')]:
   L(key+'_proposal_third_party_'+response+'_name','Imperial demand — '+en,'Demande impériale — '+fr)
   L(key+'_proposal_third_party_'+response+'_desc',"[TARGET_COUNTRY.GetName] has "+en+" the imperial demand from [INITIATOR_COUNTRY.GetName].","[TARGET_COUNTRY.GetName] a "+fr+" la demande impériale de [INITIATOR_COUNTRY.GetName].")
  for response,en,fr in [('declined','Refused','Refusée'),('accepted','Accepted','Acceptée')]:
   L(key+'_proposal_'+response+'_name',label.capitalize()+' — '+en,frlabel.capitalize()+' — '+fr)
   if response=='accepted':
    L(key+'_proposal_'+response+'_desc',"[TARGET_COUNTRY.GetName] has accepted our demand. The council’s settlement notice records the subjects or provinces concerned.","[TARGET_COUNTRY.GetName] a accepté notre demande. L’avis de règlement du conseil précise les sujets ou provinces concernés.")
   elif 'subject_release' in key:
    L(key+'_proposal_'+response+'_desc',"[TARGET_COUNTRY.GetName] has refused to release the imperial estates. Use Imperial Liberation and select the subject to free, not the foreign overlord’s homeland. Imperial Restitution is available only for registered imperial provinces actually held by that power. Existing truces and normal diplomatic restrictions remain binding.","[TARGET_COUNTRY.GetName] a refusé de libérer les États impériaux. Utilisez Libération impériale et sélectionnez le sujet à libérer, pas le territoire national du suzerain étranger. Rétrocession impériale ne vise que des provinces impériales enregistrées réellement détenues par cette puissance. Les trêves et restrictions diplomatiques normales restent applicables.")
   else:
    L(key+'_proposal_'+response+'_desc',"[TARGET_COUNTRY.GetName] has refused the territorial summons. Use Imperial Restitution on the disputed imperial state. An imperial member protected by an obligation may refuse without granting a casus belli. Existing truces remain binding.","[TARGET_COUNTRY.GetName] a refusé la sommation territoriale. Utilisez Rétrocession impériale sur l’État impérial disputé. Un membre protégé par une obligation peut refuser sans ouvrir de casus belli. Les trêves existantes restent applicables.")
 # A subject-release refusal grants liberation. If the same outside power
 # directly holds registered imperial provinces, that refusal also supports
 # their restitution. Never fabricate a territorial claim on Scandinavia.
 eligible='''aor1776_hre_emperor = yes
 scope:target_country = { aor1776_hre_member = no }
 scope:target_state = {
  owner = scope:target_country
  aor1776_hre_restitution_state = yes
  custom_tooltip = { text = aor1776_hre_restitution_refusal_valid_tt
   OR = {
    AND = { has_variable = aor1776_hre_refusal_holder var:aor1776_hre_refusal_holder ?= scope:target_country }
    scope:target_country = { has_variable = aor1776_hre_release_refused }
   }
  }
 }'''
 for field in ['possible','valid']:
  files[WG]=child(files[WG],'aor1776_hre_restitution',field,field+' = { '+eligible+' }')
 L('aor1776_hre_restitution_refusal_valid_tt','The current foreign holder has refused the relevant imperial demand within the last ten years.','Le détenteur étranger actuel a refusé la demande impériale correspondante au cours des dix dernières années.')
 L('dp_aor1776_hre_restitution_tooltip','Restore wrongfully held registered imperial provinces. Select a disputed imperial state, not an arbitrary foreign province. To free an imperial subject, use Imperial Liberation and select that subject.','Restituer les provinces impériales enregistrées détenues indûment. Sélectionner un État impérial disputé, pas une province étrangère quelconque. Pour libérer un sujet impérial, utiliser Libération impériale et sélectionner ce sujet.')
 # Replace bare-variable instructions in event acknowledgements as well.
 for num in [31,33]:
  key=f'aor1776_hre.{num}.result'
  if num==31:
   L(key,"The imperial liberation casus belli is available for the listed subjects for ten years. Select the subject as the target. If the refusing power directly holds disputed imperial provinces, restitution is also available on those states. Normal truces are not bypassed.","Le casus belli de libération impériale est ouvert pendant dix ans pour les sujets listés. Sélectionnez le sujet comme cible. Si la puissance ayant refusé détient directement des provinces impériales disputées, la rétrocession est aussi ouverte sur ces États. Les trêves ordinaires ne sont pas contournées.")
  else:
   L(key,"An external holder’s refusal opens restitution on the listed imperial provinces for ten years; a member protected by an obligation may refuse without a casus belli. Select the disputed imperial state, and respect any existing truce.","Le refus d’un détenteur extérieur ouvre la rétrocession sur les provinces impériales listées pendant dix ans ; un membre protégé par une obligation peut refuser sans casus belli. Sélectionnez l’État impérial disputé et respectez toute trêve existante.")
 # Scope-preserving event text, with names still provided by saved reply lists.
 L('aor1776_hre.31.d',"[SCOPE.sCountry('hre_reply_holder').GetName] has refused to release the imperial estates. The council may seek their liberation; the settlement list names each estate whose foreign dependency is disputed.","[SCOPE.sCountry('hre_reply_holder').GetName] a refusé de libérer les États impériaux. Le conseil peut poursuivre leur libération ; la liste du règlement désigne chaque État dont la dépendance étrangère est contestée.")
 for lang,idx in [('english',0),('french',1)]:
  for rel,raw in list(files.items()):
   if rel.startswith('localization/'+lang+'/'):
    files[rel]='\n'.join(line for line in raw.split('\n') if not any(re.match(r'\s*'+re.escape(k)+r':',line) for k in loc))
  files[f'localization/{lang}/1776_imperial_demand_feedback_l_{lang}.yml']='\ufeffl_'+lang+':\n'+''.join(' '+k+':0 "'+v[idx].replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items())
 return files
