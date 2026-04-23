# Logical Data Model: Direct-to-Consumer Life Insurance Customer Segmentation

**Use case:** Simplified-issue term and whole life policies sold through an affinity partnership (e.g., AARP/New York Life model). 850K active policyholders. 78% lapse rate over 10 years. Goals: reduce early-term lapse + identify high-value prospect segments for digital acquisition.

**Data available:** Application data, policy data, payment history, call center logs. No psychographic data.

---

## Entity Overview

| Entity | Purpose | Primary Data Source |
|--------|---------|-------------------|
| Person | Central identity record | CRM / application data |
| Applicant | Application-stage record (pre-policy) | Application system |
| Application | Full application and underwriting record | Application system |
| Policy | Active or historical policy record | Policy administration system |
| Product | Product catalog (term / whole life) | Policy administration system |
| Payment | Individual payment transactions | Billing / payment processor |
| PaymentSummary | Aggregated payment behavior per policy | Derived from Payment |
| LapseEvent | Record of every lapse occurrence | Policy administration system |
| Reinstatement | Re-activation after lapse | Policy administration system |
| InteractionCallCenter | Every inbound and outbound contact | Call center / CRM |
| AffinityPartner | Partnership organization record | Partner management system |
| AffinityMember | Individual member of an affinity partner | Partner data feed |
| MarketingCampaign | Campaign-level metadata and results | Marketing automation / CRM |
| InteractionDigital | Pre-application web/digital engagement | Web analytics |
| CustomerInteraction | Cross-channel interaction event hub; unified timeline across all touchpoints | CRM / derived |
| Beneficiary | Named beneficiary on a policy | Policy administration system |
| Agent | Call center rep or licensed agent | HR / licensing system |
| Rider | Catalog of available riders and benefit options | Policy administration system |
| PolicyRider | Junction: which riders are attached to a policy | Policy administration system |
| PolicyChange | Every mid-term policy modification (face amount, frequency, etc.) | Policy administration system |
| PolicyConversion | Term-to-permanent conversion event | Policy administration system |
| InteractionDirectMail | Outbound mail pieces sent + inbound responses (reply card, BRC, returned form); covers acquisition, service, billing, retention, and upsell mail | Mail fulfillment / scanning system |

---

## Entities and Attributes

### 1. PERSON
Core identity record. One record per individual, regardless of how many policies or applications they have.

| Attribute | Type | Notes |
|-----------|------|-------|
| person_id | UUID (PK) | Internal unique identifier |
| first_name | String | |
| last_name | String | |
| date_of_birth | Date | Critical for age-band segmentation |
| age | Integer | Derived from DOB; recalculate on anniversary |
| gender | Enum | M / F / Unknown |
| marital_status | Enum | Single / Married / Widowed / Divorced / Unknown |
| address_street | String | |
| address_city | String | |
| address_state | String | Two-letter state code |
| address_zip | String | Five-digit; key for geographic + income proxy |
| email_address | String | Nullable; not all customers provide |
| phone_primary | String | |
| phone_type | Enum | Mobile / Landline / Unknown |
| preferred_contact_method | Enum | Mail / Phone / Email / None |
| email_opt_in_flag | Boolean | CAN-SPAM compliance |
| sms_opt_in_flag | Boolean | TCPA compliance |
| do_not_contact_flag | Boolean | Legal / regulatory override |
| affinity_member_id | FK → AffinityMember | Null if not an affinity member |
| record_source | Enum | Application / Partner_Feed / Call_Center |
| record_created_date | Timestamp | |
| record_updated_date | Timestamp | |

**Segmentation signals:** age, gender, marital_status, address_zip (income proxy), preferred_contact_method

---

### 2. APPLICATION
Full record of every application submitted, including declined and withdrawn.

| Attribute | Type | Notes |
|-----------|------|-------|
| application_id | UUID (PK) | |
| person_id | FK → Person | |
| product_id | FK → Product | |
| affinity_partner_id | FK → AffinityPartner | |
| campaign_id | FK → MarketingCampaign | Source campaign |
| digital_session_id | FK → InteractionDigital | Null if not a digital application |
| agent_id | FK → Agent | Null if fully self-serve |
| application_date | Date | |
| application_channel | Enum | Web / Phone / Mail / In-Person |
| product_type_requested | Enum | Term / WholeLife |
| coverage_amount_requested | Decimal | Face amount applied for |
| payment_frequency_requested | Enum | Monthly / Quarterly / Semi-Annual / Annual |
| payment_method_selected | Enum | EFT / Check / CreditCard / DebitCard |
| tobacco_use_flag | Boolean | Simplified issue health question |
| beneficiary_relationship | String | Relationship to first-named beneficiary |
| underwriting_decision | Enum | Approved / Declined / Referred / Withdrawn |
| underwriting_decision_date | Date | |
| decline_reason_code | String | Null if approved |
| policy_id | FK → Policy | Null if not approved / not yet issued |
| time_to_decision_days | Integer | Derived: decision_date − application_date |
| is_replacement_policy | Boolean | Replacing existing life insurance |
| prior_policy_id | FK → Policy | Null if not replacement |
| application_role | Enum | Primary / Spouse — Primary = primary group member; Spouse = spouse applying simultaneously |
| linked_application_id | FK → Application | For spouse applications: FK to the primary member's application submitted in the same session; null if Primary |
| primary_person_id | FK → Person | For spouse applications: Person record of the primary group member; null if Primary role |
| household_link_id | UUID | Shared identifier grouping a primary + spouse application pair in the same session |

**Segmentation signals:** application_channel, payment_method_selected, coverage_amount_requested, time_to_decision_days, is_replacement_policy, tobacco_use_flag, application_role

---

### 3. POLICY
One record per policy. The central operational entity.

| Attribute | Type | Notes |
|-----------|------|-------|
| policy_id | UUID (PK) | |
| person_id | FK → Person | |
| application_id | FK → Application | |
| product_id | FK → Product | |
| affinity_partner_id | FK → AffinityPartner | |
| agent_id | FK → Agent | |
| policy_number | String | External policy number |
| policy_status | Enum | Active / Lapsed / Surrendered / Matured / PaidUp / DeathClaim / Cancelled |
| issue_date | Date | Date policy was issued |
| effective_date | Date | Coverage start date |
| expiration_date | Date | Null for whole life; term end date |
| anniversary_date | Date | Annual review date |
| face_amount | Decimal | Coverage amount issued (may differ from requested) |
| modal_premium | Decimal | Premium per payment interval |
| payment_frequency | Enum | Monthly / Quarterly / Semi-Annual / Annual |
| annual_premium | Decimal | Derived: modal_premium × payment_frequency_factor |
| payment_method | Enum | EFT / Check / CreditCard / DebitCard |
| eft_enrollment_flag | Boolean | True if on automatic bank draft |
| issue_state | String | State of policy issue |
| underwriting_class | String | Simplified issue class assigned |
| policy_year_current | Integer | Derived: years since issue_date |
| product_type | Enum | SimplifiedTerm / SimplifiedWholeLife |
| issue_age | Integer | Age at issue_date |
| issue_age_band | Enum | 45-49 / 50-54 / 55-59 / 60-64 / 65-69 / 70-74 / 75+ |
| lapse_date | Date | Null if still active |
| lapse_policy_year | Integer | Derived: policy year when lapsed |
| surrender_date | Date | Null if not surrendered |
| surrender_value | Decimal | Cash value at surrender |
| death_claim_date | Date | Null if no claim |
| channel | Enum | DirectMail / Digital / Inbound_Phone / Outbound_Phone |
| is_reinstated_policy | Boolean | True if ever lapsed and reinstated |
| reinstatement_count | Integer | Number of times reinstated |
| conversion_flag | Boolean | True if this policy is the result of a term-to-perm conversion |
| converted_from_policy_id | FK → Policy | Source term policy; null if not a conversion |
| original_product_type | Enum | Product type before conversion; null if not converted |
| current_face_amount | Decimal | Current face amount; may differ from face_amount at issue due to changes |
| policy_change_count | Integer | Total mid-term policy changes (face amount, frequency, etc.) |
| rider_count | Integer | Count of active riders at present |
| household_link_id | UUID | Shared ID linking primary + spouse policies issued in the same session |

**Segmentation signals:** product_type, payment_method, eft_enrollment_flag, face_amount, annual_premium, issue_age_band, channel, issue_state, lapse_policy_year, reinstatement_count, conversion_flag, rider_count, household_link_id

---

### 4. PRODUCT
Product catalog. Relatively static reference data.

| Attribute | Type | Notes |
|-----------|------|-------|
| product_id | UUID (PK) | |
| product_name | String | |
| product_type | Enum | SimplifiedTerm / SimplifiedWholeLife |
| issue_age_min | Integer | Minimum eligible issue age |
| issue_age_max | Integer | Maximum eligible issue age |
| face_amount_min | Decimal | |
| face_amount_max | Decimal | |
| term_length_years | Integer | Null for whole life |
| underwriting_type | Enum | SimplifiedIssue / GuaranteedIssue |
| product_status | Enum | Active / Discontinued |
| launch_date | Date | |
| discontinue_date | Date | Null if still active |
| target_age_band | String | Primary age target (e.g., "50-75") |
| affinty_partner_exclusive | Boolean | Partner-exclusive product |

---

### 5. PAYMENT
One record per payment transaction attempt — including failures.

| Attribute | Type | Notes |
|-----------|------|-------|
| payment_id | UUID (PK) | |
| policy_id | FK → Policy | |
| person_id | FK → Person | |
| payment_due_date | Date | When premium was due |
| payment_date | Date | Actual processing date; null if unpaid |
| payment_amount | Decimal | |
| payment_method | Enum | EFT / Check / CreditCard / DebitCard / MoneyOrder |
| payment_channel | Enum | AutoPay / Online / Phone / Mail |
| payment_status | Enum | Paid / Returned / Failed / Reversed / Waived |
| return_reason_code | Enum | NSF / AccountClosed / InvalidAccount / StopPayment / Null |
| days_late | Integer | Derived: payment_date − payment_due_date; negative if early |
| grace_period_flag | Boolean | True if paid within grace period (typically 31 days) |
| reinstatement_payment_flag | Boolean | True if payment reinstated a lapsed policy |
| policy_period | Integer | Which premium period this payment covers |
| payment_year | Integer | Calendar year of payment |

**Segmentation signals:** payment_method, payment_status, return_reason_code, days_late, grace_period_flag, payment_channel

---

### 6. PAYMENT_SUMMARY
Aggregated payment behavior per policy. Pre-computed for segmentation and scoring. Rebuilt at each analysis run.

| Attribute | Type | Notes |
|-----------|------|-------|
| policy_id | FK → Policy (PK) | One record per policy |
| total_premiums_due | Integer | Count of scheduled payments |
| total_premiums_paid | Integer | Count of successful payments |
| total_premiums_returned | Integer | Count of returned/failed payments |
| payment_rate | Decimal | total_premiums_paid / total_premiums_due |
| on_time_payment_rate | Decimal | % paid on or before due date |
| grace_period_usage_count | Integer | Times paid within grace period (not on time) |
| max_consecutive_missed | Integer | Longest streak of missed payments |
| current_consecutive_missed | Integer | Active streak of missed payments |
| total_nsf_count | Integer | Total returned/NSF transactions |
| payment_method_change_count | Integer | Times payment method changed |
| avg_days_late | Decimal | Average days late across all payments |
| last_payment_date | Date | Most recent successful payment |
| last_payment_method | Enum | Method used for last payment |
| eft_enrollment_ever | Boolean | Ever enrolled in EFT |
| current_eft_enrollment | Boolean | Currently on EFT |
| eft_disenrollment_count | Integer | Times removed from EFT |
| first_missed_payment_policy_month | Integer | Which policy month first payment missed |
| total_premium_revenue | Decimal | Sum of all paid premium amounts |
| payment_consistency_score | Decimal | Composite: on-time rate + no NSF + EFT enrolled (0–100) |

**Segmentation signals:** payment_rate, on_time_payment_rate, max_consecutive_missed, total_nsf_count, eft_enrollment_ever, payment_method_change_count, first_missed_payment_policy_month, payment_consistency_score

---

### 7. LAPSE_EVENT
One record per lapse occurrence. A policy can have multiple lapse events if it was reinstated and lapsed again.

| Attribute | Type | Notes |
|-----------|------|-------|
| lapse_event_id | UUID (PK) | |
| policy_id | FK → Policy | |
| person_id | FK → Person | |
| lapse_date | Date | |
| lapse_reason_code | Enum | NonPayment / VoluntarySurrender / NonRenewal / Unknown |
| lapse_policy_year | Integer | Policy year (1-10) when lapse occurred |
| lapse_policy_month | Integer | Policy month (1-120) when lapse occurred |
| early_lapse_flag | Boolean | True if lapse_policy_month ≤ 24 |
| premiums_paid_count | Integer | Total premiums paid before lapse |
| premium_revenue_to_lapse | Decimal | Total premium revenue collected before lapse |
| final_payment_method | Enum | Payment method at time of lapse |
| missed_payments_before_lapse | Integer | Count of missed/failed payments before lapse |
| prior_nsf_count | Integer | NSF count before lapse |
| grace_period_expired_flag | Boolean | True if lapse triggered by grace period expiry |
| cancellation_request_flag | Boolean | True if customer explicitly requested cancellation |
| retention_call_attempt_flag | Boolean | True if outbound retention call was attempted |
| retention_outcome | Enum | Saved / Lapsed / NoContact |
| subsequent_reinstatement_flag | Boolean | True if policy was later reinstated |
| days_lapsed | Integer | Days between lapse and reinstatement; null if not reinstated |

**Segmentation signals:** lapse_policy_year, lapse_policy_month, early_lapse_flag, lapse_reason_code, missed_payments_before_lapse, prior_nsf_count, cancellation_request_flag, retention_outcome

---

### 8. REINSTATEMENT
Tracks policies reinstated after lapse.

| Attribute | Type | Notes |
|-----------|------|-------|
| reinstatement_id | UUID (PK) | |
| policy_id | FK → Policy | |
| lapse_event_id | FK → LapseEvent | |
| reinstatement_date | Date | |
| days_lapsed_before_reinstatement | Integer | Derived: reinstatement_date − lapse_date |
| reinstatement_trigger | Enum | RetentionCall / WinBackCampaign / SelfInitiated / Unknown |
| reinstatement_channel | Enum | Phone / Online / Mail |
| reinstatement_amount_paid | Decimal | Back-premiums + interest/fees |
| new_payment_method | Enum | Method after reinstatement |
| eft_enrolled_at_reinstatement | Boolean | Enrolled in EFT at time of reinstatement |
| subsequent_lapse_flag | Boolean | Lapsed again after this reinstatement |
| subsequent_lapse_date | Date | Null if still active |
| months_active_post_reinstatement | Integer | Months remained active after reinstatement |

---

### 9. INTERACTION_CALL_CENTER
One record per inbound or outbound contact event.

| Attribute | Type | Notes |
|-----------|------|-------|
| interaction_id | UUID (PK) | |
| person_id | FK → Person | |
| policy_id | FK → Policy | Null if pre-sale or prospect call |
| agent_id | FK → Agent | Null if IVR-only resolution |
| interaction_datetime | Timestamp | |
| interaction_type | Enum | Inbound / Outbound |
| outbound_campaign_id | FK → MarketingCampaign | Null if inbound |
| call_duration_seconds | Integer | |
| ivr_time_seconds | Integer | Time in IVR before agent |
| ivr_resolution_flag | Boolean | Resolved without live agent |
| call_reason_primary | Enum | BillingInquiry / PaymentChange / CoverageQuestion / CancellationRequest / LapseNotice / ReinstatementInquiry / BeneficiaryChange / AddressChange / NewSale / Complaint / Claim / Other |
| call_reason_secondary | String | Free text or secondary coded reason |
| call_outcome | Enum | Resolved / Transferred / CallbackScheduled / PolicyCancelled / ReinstatementCompleted / SaleCompleted / Escalated / NoResolution |
| cancellation_intent_flag | Boolean | Customer expressed intent to cancel |
| save_attempt_flag | Boolean | Agent attempted retention save |
| save_successful_flag | Boolean | Null if no save attempt made |
| policy_year_at_contact | Integer | Policy year when call occurred |
| escalation_flag | Boolean | Escalated to supervisor or specialist |
| sentiment_score | Decimal | 1-5 scale; null if speech analytics not applied |
| call_topics_list | String | Pipe-delimited list of NLP-tagged topics |
| policy_status_at_contact | Enum | Status of policy at time of call |
| customer_interaction_id | FK → CustomerInteraction | Hub record linking this call to the cross-channel interaction timeline; null if hub not yet provisioned |

**Segmentation signals:** call_reason_primary, cancellation_intent_flag, call_outcome, policy_year_at_contact, save_successful_flag, call_topics_list (NLP-derived)

---

### 10. AFFINITY_PARTNER
One record per affinity organization.

| Attribute | Type | Notes |
|-----------|------|-------|
| partner_id | UUID (PK) | |
| partner_name | String | |
| partner_type | Enum | MembershipAssociation / Employer / Union / Other |
| partnership_start_date | Date | |
| partnership_status | Enum | Active / Inactive |
| total_member_count | Integer | Total eligible universe |
| active_policyholder_count | Integer | Members who hold active policies |
| penetration_rate | Decimal | active_policyholder_count / total_member_count |
| primary_age_range_min | Integer | Member demographic |
| primary_age_range_max | Integer | Member demographic |
| primary_channel | Enum | Mail / Digital / Both |
| geographic_coverage | String | National / Regional / specific states |
| renewal_date | Date | Partnership contract renewal |

---

### 11. AFFINITY_MEMBER
Individual member record from affinity partner. Represents the prospect universe before acquisition.

| Attribute | Type | Notes |
|-----------|------|-------|
| member_id | UUID (PK) | |
| partner_id | FK → AffinityPartner | |
| person_id | FK → Person | Null until matched to internal record |
| membership_join_date | Date | |
| membership_status | Enum | Active / Lapsed |
| membership_tier | String | If partner uses tier levels |
| age | Integer | As provided by partner |
| gender | String | As provided by partner |
| zip_code | String | |
| state | String | |
| policyholder_flag | Boolean | Has purchased a policy from this program |
| application_submitted_flag | Boolean | Ever submitted an application |
| solicitations_received_count | Integer | Total marketing touches received |
| last_solicitation_date | Date | |
| solicitation_response_flag | Boolean | Ever responded to a solicitation |
| last_response_date | Date | |
| do_not_mail_flag | Boolean | Suppressed from direct mail |
| do_not_email_flag | Boolean | Suppressed from email |

**Segmentation signals:** membership_status, age, zip_code, solicitations_received_count, solicitation_response_flag, policyholder_flag

---

### 12. MARKETING_CAMPAIGN
One record per campaign execution, including both acquisition and retention campaigns.

| Attribute | Type | Notes |
|-----------|------|-------|
| campaign_id | UUID (PK) | |
| campaign_name | String | |
| campaign_type | Enum | DirectMail / Email / DigitalDisplay / PaidSearch / Social / Outbound_Phone / SMS |
| campaign_objective | Enum | Acquisition / EarlyLapseRetention / WinBack / Upsell / Reactivation |
| launch_date | Date | |
| end_date | Date | |
| partner_id | FK → AffinityPartner | Null if not partner-specific |
| target_segment_description | String | Who was targeted |
| target_age_band | String | |
| offer_type | String | Rate emphasis, product feature, coverage amount |
| creative_version | String | A/B test version identifier |
| universe_size | Integer | Total names mailed/contacted |
| response_count | Integer | |
| response_rate | Decimal | Derived |
| application_count | Integer | |
| application_rate | Decimal | Derived |
| issued_policy_count | Integer | |
| issue_rate | Decimal | Derived |
| cost_per_issued_policy | Decimal | |
| eft_enrollment_rate | Decimal | % of issued policies enrolled in EFT |

---

### 13. INTERACTION_DIGITAL
Web and digital engagement events. May be anonymous until an application is started.

| Attribute | Type | Notes |
|-----------|------|-------|
| session_id | UUID (PK) | |
| person_id | FK → Person | Null if anonymous/pre-identification |
| application_id | FK → Application | Null if no application started |
| session_date | Date | |
| session_datetime | Timestamp | |
| device_type | Enum | Desktop / Mobile / Tablet |
| browser | String | |
| acquisition_channel | Enum | OrganicSearch / PaidSearch / Email / Social / DirectMail_QR / DirectType_In / Referral / Display |
| utm_source | String | |
| utm_medium | String | |
| utm_campaign | String | FK-equivalent to MarketingCampaign |
| landing_page | String | URL path |
| page_views_count | Integer | |
| session_duration_seconds | Integer | |
| quote_started_flag | Boolean | |
| quote_completed_flag | Boolean | |
| application_started_flag | Boolean | |
| application_completed_flag | Boolean | |
| drop_off_step | String | Last step completed before abandonment |
| return_visit_flag | Boolean | Not first session |
| prior_session_count | Integer | Total prior sessions for this device/user |
| ip_geolocation_state | String | Approximate state from IP |
| ip_geolocation_zip | String | Approximate zip from IP |
| customer_interaction_id | FK → CustomerInteraction | Hub record linking this session to the cross-channel interaction timeline; null if hub not yet provisioned |

**Segmentation signals:** acquisition_channel, device_type, quote_completed_flag, application_completed_flag, drop_off_step, return_visit_flag

---

### 14. BENEFICIARY
Named beneficiary(ies) on a policy.

| Attribute | Type | Notes |
|-----------|------|-------|
| beneficiary_id | UUID (PK) | |
| policy_id | FK → Policy | |
| beneficiary_type | Enum | Primary / Contingent |
| relationship_to_insured | Enum | Spouse / Child / Parent / Sibling / Other_Family / NonFamily |
| allocation_percentage | Decimal | Must sum to 100 across primary beneficiaries |

**Segmentation signals:** relationship_to_insured (indicator of household structure / life stage)

---

### 15. AGENT
Call center representative or licensed agent record.

| Attribute | Type | Notes |
|-----------|------|-------|
| agent_id | UUID (PK) | |
| agent_type | Enum | CallCenter_Sales / CallCenter_Service / CallCenter_Retention / Field |
| states_licensed | String | Pipe-delimited list of state licenses |
| hire_date | Date | |
| tenure_months | Integer | Derived |
| active_flag | Boolean | |
| team | String | Sales / Service / Retention / etc. |

---

### 16. RIDER
Catalog of available riders and benefit add-ons. Reference data shared across all policies.

| Attribute | Type | Notes |
|-----------|------|-------|
| rider_id | UUID (PK) | |
| rider_name | String | |
| rider_type | Enum | WaiverOfPremium / AccidentalDeathBenefit / ChildTerm / ReturnOfPremium / AcceleratedDeathBenefit / LongTermCare / Other |
| rider_description | String | |
| premium_basis | Enum | FlatFee / PerThousandFaceAmount / PercentOfBasePremium |
| product_eligibility | String | Pipe-delimited list of product_ids this rider is available on |
| issue_age_max | Integer | Maximum age at which this rider can be added |
| rider_status | Enum | Active / Discontinued |

---

### 17. POLICY_RIDER
Junction entity: every rider attached to every policy. One record per rider per policy.

| Attribute | Type | Notes |
|-----------|------|-------|
| policy_rider_id | UUID (PK) | |
| policy_id | FK → Policy | |
| rider_id | FK → Rider | |
| rider_status | Enum | Active / Terminated / Lapsed |
| add_date | Date | Date rider was added to the policy |
| add_channel | Enum | AtIssue / Phone / Mail / Online |
| termination_date | Date | Null if still active |
| termination_reason | Enum | PolicyLapse / VoluntaryRemoval / AgeOut / ClaimPaid / Null |
| rider_face_amount | Decimal | Coverage amount for riders with their own limit (e.g., ADB); null if not applicable |
| rider_annual_premium | Decimal | Incremental premium for this rider |
| rider_claim_filed_flag | Boolean | A benefit claim was filed under this rider |
| rider_claim_date | Date | Date benefit claim filed; null if no claim |
| wop_trigger_date | Date | Date waiver of premium was triggered; null unless WOP rider and claim filed |
| wop_active_flag | Boolean | Premium waiver currently in force |
| policy_year_at_add | Integer | Policy year when rider was added |

**Segmentation signals:** rider_type, add_channel, policy_year_at_add, rider_claim_filed_flag, wop_active_flag, rider_annual_premium

---

### 18. POLICY_CHANGE
One record per mid-term policy modification. Captures face amount changes, payment method changes, frequency changes, rider additions/removals, and beneficiary changes.

| Attribute | Type | Notes |
|-----------|------|-------|
| change_id | UUID (PK) | |
| policy_id | FK → Policy | |
| person_id | FK → Person | |
| agent_id | FK → Agent | Null if self-service |
| change_date | Date | |
| change_type | Enum | FaceAmountIncrease / FaceAmountDecrease / PaymentFrequencyChange / PaymentMethodChange / BeneficiaryChange / AddressChange / RiderAdded / RiderRemoved / NameChange / Other |
| change_channel | Enum | Phone / Online / Mail / Agent |
| policy_year_at_change | Integer | Policy year when change was made |
| prior_face_amount | Decimal | Null if not a face amount change |
| new_face_amount | Decimal | Null if not a face amount change |
| face_amount_delta | Decimal | Derived: new_face_amount − prior_face_amount; null if not applicable |
| face_change_direction | Enum | Increase / Decrease / Null |
| underwriting_required_flag | Boolean | Face amount increase above simplified-issue limits requires re-underwriting |
| underwriting_decision | Enum | Approved / Declined / Null |
| prior_annual_premium | Decimal | Annual premium before change |
| new_annual_premium | Decimal | Annual premium after change |
| premium_delta | Decimal | Derived: new_annual_premium − prior_annual_premium |
| campaign_id | FK → MarketingCampaign | Null unless change was triggered by a campaign (e.g., upsell coverage mailer) |
| rider_id | FK → Rider | For RiderAdded / RiderRemoved change types; null otherwise |

**Segmentation signals:** change_type, face_change_direction, policy_year_at_change, campaign_id (campaign-driven vs. self-initiated), underwriting_required_flag

---

### 19. POLICY_CONVERSION
Tracks every term-to-permanent conversion event. One record per conversion.

| Attribute | Type | Notes |
|-----------|------|-------|
| conversion_id | UUID (PK) | |
| source_policy_id | FK → Policy | The term policy being converted |
| converted_policy_id | FK → Policy | The new whole life policy issued |
| person_id | FK → Person | |
| agent_id | FK → Agent | Null if self-service |
| conversion_date | Date | |
| conversion_type | Enum | TermToWholeLife (extend if other conversion types exist) |
| conversion_channel | Enum | Phone / Mail / Online / Agent |
| source_policy_year_at_conversion | Integer | How many years into the term policy when conversion occurred |
| source_face_amount | Decimal | Face amount of the source term policy |
| converted_face_amount | Decimal | Face amount of the new whole life policy |
| face_amount_delta_at_conversion | Decimal | Derived: converted − source |
| source_annual_premium | Decimal | Term premium before conversion |
| new_annual_premium | Decimal | Whole life premium after conversion |
| premium_increase_at_conversion | Decimal | Derived: new − source |
| conversion_trigger | Enum | CustomerInitiated / RetentionCall / Campaign / NearTermExpiry / Unknown |
| campaign_id | FK → MarketingCampaign | Null if not campaign-driven |
| riders_transferred_flag | Boolean | Riders from term policy carried over to new whole life policy |
| underwriting_required_flag | Boolean | Conversion type required new underwriting |

**Segmentation signals:** source_policy_year_at_conversion, conversion_trigger, premium_increase_at_conversion, face_amount_delta_at_conversion, conversion_channel, riders_transferred_flag

---

### 20. CUSTOMER_INTERACTION
Cross-channel interaction hub. One record per interaction event, regardless of channel. Provides a unified, chronologically ordered timeline of every touchpoint for a person. Links to channel-specific detail entities (InteractionCallCenter, InteractionDigital) for full attribute access. Designed to be extensible as new interaction channels are instrumented.

| Attribute | Type | Notes |
|-----------|------|-------|
| customer_interaction_id | UUID (PK) | |
| person_id | FK → Person | |
| policy_id | FK → Policy | Null for pre-policy / prospect interactions |
| interaction_datetime | Timestamp | Canonical timestamp for timeline ordering |
| interaction_date | Date | Calendar date; derived from interaction_datetime |
| channel_type | Enum | Phone / Digital / DirectMail / DirectMail_Response / Email_Click / SMS_Response / OutboundCall / Agent / Unknown; DirectMail = outbound piece sent; DirectMail_Response = inbound reply received; extensible as new channels are added |
| interaction_category | Enum | Acquisition / NewPolicyholder / Service / Billing / Retention / WinBack / Upsell / Conversion / Claim / Complaint / Unknown |
| journey_stage | Enum | Prospect / Applicant / NewPolicyholder_Yr1 / Established / AtRisk / Lapsed / Converted |
| is_inbound | Boolean | True if customer-initiated; False if company-initiated (outbound) |
| interaction_outcome | Enum | Purchased / Applied / Engaged / Resolved / Escalated / Abandoned / Saved / NoContact / Unknown |
| call_center_interaction_id | FK → InteractionCallCenter | Populated when channel_type = Phone; links to full call detail; null otherwise |
| digital_session_id | FK → InteractionDigital | Populated when channel_type = Digital; links to full session detail; null otherwise |
| direct_mail_interaction_id | FK → InteractionDirectMail | Populated when channel_type = DirectMail or DirectMail_Response; links to full mail piece / response detail; null otherwise |
| campaign_id | FK → MarketingCampaign | Populated when interaction was triggered by or attributed to a campaign; null otherwise |
| policy_year_at_interaction | Integer | Policy year when interaction occurred; null for pre-policy / prospect |
| days_since_policy_issue | Integer | Derived: interaction_date − policy effective_date; null for pre-policy |
| days_since_prior_interaction | Integer | Derived: gap in days from the previous CustomerInteraction for this person; null for first-ever interaction |
| sequence_number | Integer | Ordinal position in this person's full interaction history (1 = first ever) |

**Segmentation signals:** channel_type, interaction_category, journey_stage, is_inbound, interaction_outcome, policy_year_at_interaction, days_since_prior_interaction, sequence_number

---

### 21. INTERACTION_DIRECT_MAIL
One record per direct mail event — both outbound pieces sent to a person and inbound responses (reply card, BRC, returned form, phone response to a mail piece). Covers acquisition mailings, service notices, billing notices, retention offers, and upsell/conversion mailers.

| Attribute | Type | Notes |
|-----------|------|-------|
| direct_mail_interaction_id | UUID (PK) | |
| person_id | FK → Person | |
| member_id | FK → AffinityMember | Null if person is a policyholder (not just prospect) |
| policy_id | FK → Policy | Null for prospect mailings |
| campaign_id | FK → MarketingCampaign | |
| customer_interaction_id | FK → CustomerInteraction | Hub record; null if hub not yet provisioned |
| mail_direction | Enum | Outbound / InboundResponse |
| mail_date | Date | Date piece was mailed (Outbound) or date response was received/processed (InboundResponse) |
| mail_piece_type | Enum | AcquisitionOffer / ServiceNotice / BillingNotice / RetentionOffer / WinBackOffer / UpsellOffer / ConversionOffer / StatementInsert / Other |
| package_version | String | Creative/offer version code; links to A/B test tracking |
| postage_class | Enum | FirstClass / BulkPresort / Standard |
| response_type | Enum | ReplyCard / BRC / PhoneCall / OnlineResponse / ReturnedForm / Null (Outbound only) |
| response_channel | Enum | Mail / Phone / Web / Null (for outbound records) |
| application_id | FK → Application | Populated if response resulted in a new application; null otherwise |
| policy_change_id | FK → PolicyChange | Populated if response resulted in a policy change; null otherwise |
| undeliverable_flag | Boolean | Piece returned as undeliverable |
| undeliverable_reason | Enum | AddressNotFound / MovedNoForwardingAddress / Refused / Deceased / Null |
| do_not_mail_triggered_flag | Boolean | Recipient requested removal from mail list via this interaction |
| offer_code | String | Specific offer code printed on the piece; used for response attribution |
| tracking_code | String | Unique barcode / keycode for this person+campaign combination; primary attribution key |
| ink_jet_name_flag | Boolean | Piece used personalized inkjet printing (name/coverage personalization) |
| estimated_in_home_date | Date | Expected delivery window start date |

**Segmentation signals:** mail_piece_type, mail_direction, response_type, response_channel, undeliverable_flag, application_id (null vs. populated = responded vs. not), policy_change_id

---

## Entity Relationship Map

```
AffinityPartner ──< AffinityMember >── Person
                                         │
                              ┌──────────┼──────────────────┐
                              │          │                  │
                         Application  Policy     InteractionCallCenter
                          (Primary)    │           CustomerInteraction
                                       │                    │
                              │        │                    │
                         Application  ├── Payment           │
                          (Spouse)    │        │            │
                              │       │   PaymentSummary    │
                              │       ├── LapseEvent        │
                              │       │       │             │
                              │       │   Reinstatement     │
                              │       ├── PolicyChange      │
                              │       ├── PolicyRider──< Rider
                              │       └── PolicyConversion  │
                              │           (source_policy)   │
                              │           (converted_policy)│
MarketingCampaign ────────────┴────────────────────────────-┘
        │
   InteractionDigital ───── Application
   InteractionDirectMail ── Application
        │
     Product ──< Policy
```

### Key Relationships

| From | Cardinality | To | Notes |
|------|------------|-----|-------|
| Person | 1:M | Policy | One person can hold multiple policies |
| Person | 1:M | Application | Includes declined, withdrawn, and spouse applications |
| Person | 1:M | InteractionCallCenter | Every inbound/outbound call contact |
| Person | 1:M | CustomerInteraction | Full cross-channel interaction timeline |
| Application | 1:1 | Policy | One approved application → one policy |
| Application (Primary) | 1:M | Application (Spouse) | Primary member application linked to spouse application(s) via linked_application_id |
| Application | 1:1 | household_link_id | Shared UUID groups primary + spouse applications in same session |
| Policy | 1:M | Payment | One payment per billing period |
| Policy | 1:1 | PaymentSummary | Aggregated view per policy |
| Policy | 1:M | LapseEvent | Multiple if reinstated and lapsed again |
| LapseEvent | 1:1 | Reinstatement | At most one reinstatement per lapse |
| Policy | 1:M | InteractionCallCenter | Calls referencing a specific policy |
| Policy | 1:M | CustomerInteraction | All touchpoints associated with a policy |
| Policy | 1:M | Beneficiary | Primary + contingent beneficiaries |
| Policy | M:1 | Product | Many policies per product |
| Policy | 1:M | PolicyRider | One record per rider per policy |
| PolicyRider | M:1 | Rider | Many policies can carry the same rider type |
| Policy | 1:M | PolicyChange | All mid-term modifications |
| Policy | 1:1 | PolicyConversion | As source (term being converted); null if not converted |
| PolicyConversion | 1:1 | Policy | Creates the new converted_policy_id (whole life) |
| AffinityPartner | 1:M | AffinityMember | Entire member roster |
| AffinityMember | 1:1 | Person | When member acquires a policy (matched) |
| MarketingCampaign | 1:M | Application | Campaign sourcing applications |
| MarketingCampaign | 1:M | PolicyChange | Campaign-triggered coverage change events |
| MarketingCampaign | 1:M | PolicyConversion | Campaign-triggered conversions |
| MarketingCampaign | 1:M | CustomerInteraction | Campaign-triggered interactions across all channels |
| InteractionDigital | 1:1 | Application | Session that resulted in application |
| CustomerInteraction | 1:1 | InteractionCallCenter | Detail record for phone interactions (nullable; populated when channel_type = Phone) |
| CustomerInteraction | 1:1 | InteractionDigital | Detail record for digital interactions (nullable; populated when channel_type = Digital) |
| CustomerInteraction | 1:1 | InteractionDirectMail | Detail record for direct mail interactions (nullable; populated when channel_type = DirectMail or DirectMail_Response) |
| InteractionDirectMail | M:1 | MarketingCampaign | Many mail pieces per campaign |
| InteractionDirectMail | 1:1 | Application | Mail response that converted to application (nullable) |
| InteractionDirectMail | 1:1 | PolicyChange | Mail response that resulted in a policy change (nullable) |
| Agent | 1:M | Policy | Policies sold by agent |
| Agent | 1:M | InteractionCallCenter | Interactions handled by agent |
| Agent | 1:M | PolicyConversion | Conversions facilitated by agent |

---

## Derived Metrics for Segmentation

These are calculated fields that power clustering and predictive models. They should be materialized as columns in an analytics layer (e.g., a customer 360 table), not recomputed on the fly.

### Lapse Risk Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `early_lapse_flag` | lapse_policy_month ≤ 24 | LapseEvent | Target for early-lapse prevention |
| `lapse_risk_decile` | Predicted lapse probability (1–10) | All policy + payment + call | Retention prioritization |
| `days_to_first_missed_payment` | First missed payment date − policy effective date | Payment | Leading lapse indicator |
| `payment_consistency_score` | Composite: on-time rate (50%) + no NSF (30%) + EFT enrolled (20%) | PaymentSummary | Lapse propensity proxy |
| `grace_period_dependency_rate` | grace_period_payments / total_payments | Payment | Stress signal |
| `missed_payments_policy_yr1` | Count of missed payments in policy year 1 | Payment | Strongest early-lapse predictor |
| `cancelled_intent_before_lapse` | cancellation_intent_flag = true on any call before lapse_date | InteractionCallCenter + LapseEvent | Explicit churn signal |
| `payment_method_downgrade_flag` | Switched from EFT to check after issue | PaymentSummary | Financial stress indicator |
| `lapse_policy_year_band` | 1 / 2 / 3-5 / 6-10 | LapseEvent | Lapse timing distribution |

### Customer Value Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `lifetime_premium_revenue` | Sum of all paid payment amounts | Payment | Actual value delivered |
| `projected_ltv` | annual_premium × expected_persistency_years × (1 − expense_ratio) | Policy + actuarial tables | Segment value ranking |
| `policy_persistency_yr1` | Active at 12-month anniversary | Policy | Retention benchmark |
| `policy_persistency_yr2` | Active at 24-month anniversary | Policy | Retention benchmark |
| `annual_premium_band` | <$300 / $300-$600 / $601-$1200 / >$1200 | Policy | Value tier |
| `face_amount_band` | <$10K / $10-25K / $25-50K / $50-100K / >$100K | Policy | Coverage tier |
| `multi_policy_flag` | Count of active policies > 1 | Policy | Loyalty / depth indicator |
| `reinstatement_success_flag` | Ever lapsed and successfully reinstated | LapseEvent + Reinstatement | Retention recovery signal |

### Acquisition / Prospect Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `application_completion_rate` | By channel: applications completed / started | InteractionDigital + Application | Channel quality |
| `solicitation_to_application_rate` | Applications / solicitations_received | AffinityMember + Application | Prospect responsiveness |
| `digital_engagement_score` | Sessions × (quote_completed × 2) × (app_started × 3) | InteractionDigital | Digital acquisition propensity |
| `channel_preference_score` | Modal channel across all contacts | Application + InteractionCallCenter + InteractionDigital | Preferred outreach channel |
| `age_at_issue_band` | Issue age grouped into 5-year bands | Policy | Life-stage segment |
| `issue_to_eft_rate` | % enrolled in EFT at issue by acquisition source | Policy + Application | Payment quality by source |
| `campaign_response_index` | Segment response rate / overall response rate | MarketingCampaign | Relative responsiveness |

### Payment Behavior Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `payment_method_at_issue` | Payment method selected on application | Application | Acquisition quality signal |
| `eft_conversion_rate` | % non-EFT at issue who convert to EFT | PaymentSummary | Operational opportunity |
| `nsf_rate_policy_yr1` | NSF count / premiums due in year 1 | Payment | Early lapse predictor |
| `first_year_payment_rate` | Premiums paid / premiums due in policy year 1 | Payment | Strongest lapse predictor |
| `avg_days_late_trend` | Late days in year 2 − late days in year 1 | Payment | Worsening payment behavior |
| `chronic_late_payer_flag` | avg_days_late > 15 AND grace_period_usage_count > 3 | PaymentSummary | Lapse risk + retention cost |

### Call Center Engagement Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `inbound_call_rate_yr1` | Inbound calls in policy year 1 / 12 months | InteractionCallCenter | Service complexity signal |
| `billing_inquiry_rate` | Billing calls / total calls | InteractionCallCenter | Financial confusion indicator |
| `cancellation_intent_count` | Count of calls with cancellation_intent_flag = true | InteractionCallCenter | Cumulative churn signal |
| `retention_save_rate` | Saved / attempted saves | InteractionCallCenter | Retention campaign effectiveness |
| `call_reason_profile` | Distribution of call_reason_primary codes | InteractionCallCenter | Behavioral fingerprint by segment |
| `coverage_question_flag` | Any call with reason = CoverageQuestion in year 1 | InteractionCallCenter | Engagement / confusion signal |

### Conversion & Upsell Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `conversion_flag` | Policy is result of term-to-perm conversion | Policy | Identifies converted cohort |
| `conversion_policy_year` | source_policy_year_at_conversion | PolicyConversion | When in policy lifecycle conversion happened |
| `term_to_perm_conversion_rate` | Converted policies / eligible term policies by cohort | Policy + PolicyConversion | Upsell performance by segment |
| `conversion_trigger_type` | CustomerInitiated vs. Campaign vs. NearTermExpiry | PolicyConversion | Intent and channel signal |
| `premium_increase_at_conversion` | new_annual_premium − source_annual_premium | PolicyConversion | Premium lift measurement |
| `face_amount_change_flag` | Any PolicyChange with type = FaceAmountIncrease or FaceAmountDecrease | PolicyChange | Engagement depth signal |
| `face_amount_increase_flag` | Net current_face_amount > issue face_amount | Policy + PolicyChange | Upsell / growing coverage need |
| `face_amount_decrease_flag` | Net current_face_amount < issue face_amount | Policy + PolicyChange | Financial stress / disengagement |
| `lifetime_face_amount_delta` | current_face_amount − original face_amount at issue | Policy | Net coverage trajectory |
| `coverage_change_policy_year` | Policy year when first face amount change occurred | PolicyChange | Timing of engagement |
| `campaign_driven_change_rate` | PolicyChanges with campaign_id populated / all changes | PolicyChange | Campaign upsell effectiveness |

### Rider & Benefit Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `has_any_rider_flag` | rider_count > 0 | Policy | Engagement depth; loyalty proxy |
| `rider_count_active` | Count of PolicyRider records with rider_status = Active | PolicyRider | Coverage complexity |
| `rider_premium_share` | Sum(rider_annual_premium) / annual_premium | PolicyRider + Policy | Premium depth index |
| `wop_active_flag` | Any PolicyRider where wop_active_flag = true | PolicyRider | Financial distress signal |
| `has_adb_rider` | Any active PolicyRider where rider_type = AccidentalDeathBenefit | PolicyRider | Coverage completeness |
| `has_waiver_of_premium` | Any active PolicyRider where rider_type = WaiverOfPremium | PolicyRider | Risk management profile |
| `rider_claim_rate` | Policies with rider_claim_filed_flag / policies with any rider | PolicyRider | Benefit utilization |
| `rider_added_post_issue_flag` | Any PolicyRider where add_channel ≠ AtIssue | PolicyRider | Post-issue engagement signal |

### Household & Spouse Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `spouse_policy_flag` | Person has a linked spouse policy (household_link_id match) | Policy | Household engagement depth |
| `household_policy_count` | Total active policies sharing the same household_link_id | Policy | Multi-policy household |
| `household_annual_premium` | Sum of annual_premium for all policies in household_link_id group | Policy | Household value |
| `spouse_application_rate` | Primary applications where a spouse application was also submitted | Application | Household acquisition signal |
| `spouse_conversion_rate` | Spouse applications / primary applications approved | Application | Joint acquisition effectiveness |
| `household_lapse_correlation_flag` | Primary and spouse policy both lapsed within same 90-day window | LapseEvent + Policy | Joint financial stress indicator |
| `joint_persistency_yr1` | Both household policies active at 12 months | Policy | Household retention |

### Cross-Channel Engagement Metrics

| Metric | Formula / Definition | Source Entities | Segment Use |
|--------|---------------------|----------------|-------------|
| `total_interaction_count` | Count of all CustomerInteraction records for this person | CustomerInteraction | Overall engagement volume |
| `interaction_velocity_yr1` | CustomerInteraction count in policy year 1 | CustomerInteraction | Early-life engagement density |
| `cross_channel_flag` | Person used 2+ distinct channel_type values | CustomerInteraction | Multi-channel engager |
| `days_since_last_interaction` | Days since most recent CustomerInteraction.interaction_date | CustomerInteraction | Engagement recency |
| `days_to_first_interaction_post_issue` | Earliest post-issue interaction_date − policy effective_date | CustomerInteraction + Policy | Onboarding engagement speed |
| `pre_lapse_touchpoint_count` | CustomerInteraction records in 90 days before lapse_date | CustomerInteraction + LapseEvent | Retention attempt density before lapse |
| `interaction_gap_before_lapse` | Days from last CustomerInteraction to lapse_date | CustomerInteraction + LapseEvent | Disengagement signal preceding lapse |
| `digital_to_phone_ratio` | InteractionDigital count / InteractionCallCenter count | CustomerInteraction | Self-service vs. assisted preference |
| `direct_mail_response_flag` | Any InteractionDirectMail where response_type is not null | InteractionDirectMail | Mail channel responder |
| `mail_solicitations_received` | Count of Outbound InteractionDirectMail records | InteractionDirectMail | Solicitation exposure volume |
| `mail_response_rate` | InboundResponse records / Outbound records | InteractionDirectMail | Mail channel responsiveness |
| `mail_undeliverable_flag` | Any InteractionDirectMail with undeliverable_flag = true | InteractionDirectMail | Address quality / reachability signal |
| `channel_mix_profile` | Distribution of channel_type across all CustomerInteraction records | CustomerInteraction | Multi-channel behavioral fingerprint |
| `journey_stage_at_lapse` | journey_stage at most recent CustomerInteraction before lapse_date | CustomerInteraction + LapseEvent | Journey position when customer was lost |
| `last_interaction_outcome` | interaction_outcome of most recent CustomerInteraction | CustomerInteraction | Final engagement state before analysis date |

---

## Segmentation-Ready Views

The following analytical views should be built on top of the entities above. Each powers a specific segmentation objective.

### View 1: POLICY_360
One row per policy. Full behavioral snapshot for lapse prediction and retention segmentation.

**Key columns:** policy_id, person_id, product_type, issue_age_band, face_amount_band, annual_premium_band, payment_method_at_issue, eft_enrollment_flag, channel, payment_consistency_score, first_year_payment_rate, nsf_rate_policy_yr1, missed_payments_policy_yr1, inbound_call_rate_yr1, cancellation_intent_count, policy_status, lapse_policy_year_band, early_lapse_flag, lapse_risk_decile, conversion_flag, conversion_policy_year, has_any_rider_flag, rider_count_active, rider_premium_share, wop_active_flag, face_amount_increase_flag, face_amount_decrease_flag, policy_change_count, spouse_policy_flag, household_annual_premium

**Uses:** K-means clustering for lapse risk segments, decision tree for lapse prediction model, RFM adaptation (Recency = time since last payment, Frequency = payment rate, Monetary = annual premium), conversion propensity scoring, household value segmentation

---

### View 2: PROSPECT_360
One row per affinity member who has not yet purchased. Powers digital acquisition segmentation.

**Key columns:** member_id, partner_id, age, gender, zip_code, membership_status, solicitations_received_count, solicitation_response_flag, last_response_date, do_not_mail_flag, digital_engagement_score, application_started_flag, application_completed_flag, drop_off_step, campaign_response_index, zip_median_income (appended from Census), zip_life_insurance_penetration (external data)

**Uses:** Propensity-to-buy model, digital acquisition prioritization, look-alike modeling against existing policyholders

---

### View 3: CAMPAIGN_ATTRIBUTION
One row per application with full attribution chain. Powers acquisition ROI and channel mix segmentation.

**Key columns:** application_id, campaign_id, campaign_type, acquisition_channel, digital_session_id, device_type, landing_page, utm_source, underwriting_decision, policy_issued_flag, eft_enrolled_at_issue, first_year_payment_rate, early_lapse_flag, cost_per_issued_policy

**Uses:** Cohort analysis by acquisition channel, channel quality scoring, media mix optimization

---

### View 4: LAPSE_COHORT
One row per lapsed policy with full pre-lapse behavioral history. Powers lapse timing and early warning models.

**Key columns:** policy_id, lapse_event_id, lapse_policy_month, early_lapse_flag, lapse_reason_code, payment_method_at_issue, first_year_payment_rate, missed_payments_policy_yr1, nsf_rate_policy_yr1, cancellation_intent_count, retention_call_attempt_flag, retention_outcome, issue_age_band, product_type, channel, face_amount_band

**Uses:** Survival analysis (time-to-lapse), logistic regression for lapse prediction, clustering for lapse profile types

---

### View 5: HOUSEHOLD_360
One row per household (grouped by household_link_id). Powers household-level acquisition, retention, and upsell segmentation.

**Key columns:** household_link_id, primary_person_id, spouse_person_id, primary_policy_id, spouse_policy_id, household_policy_count, household_annual_premium, primary_product_type, spouse_product_type, primary_issue_age_band, spouse_issue_age_band, primary_policy_status, spouse_policy_status, household_lapse_correlation_flag, joint_persistency_yr1, household_rider_count, household_conversion_flag, primary_channel, spouse_applied_flag, spouse_approved_flag

**Uses:** Household-level value segmentation, joint lapse risk scoring, upsell prioritization (single-policy households as conversion targets), acquisition lookalike modeling for affinity member households

---

### View 6: CONVERSION_COHORT
One row per eligible term policy (active or recently lapsed term). Powers term-to-perm conversion opportunity analysis.

**Key columns:** policy_id, person_id, product_type, issue_age_band, source_policy_year_at_conversion_eligible, face_amount_band, annual_premium_band, payment_consistency_score, has_any_rider_flag, conversion_flag, conversion_date, conversion_trigger, campaign_id, premium_increase_at_conversion, lapse_risk_decile, inbound_call_rate_yr1, cancellation_intent_count

**Uses:** Conversion propensity model, campaign targeting for upsell outreach, revenue lift sizing for conversion program

---

### View 7: CUSTOMER_JOURNEY_TIMELINE
One row per interaction event per person, ordered chronologically. Full multi-channel touchpoint sequence for journey pattern analysis and next-best-action modeling.

**Key columns:** customer_interaction_id, person_id, policy_id, interaction_datetime, channel_type, interaction_category, journey_stage, is_inbound, interaction_outcome, days_since_prior_interaction, sequence_number, policy_year_at_interaction, call_duration_seconds (from InteractionCallCenter), call_reason_primary (from InteractionCallCenter), cancellation_intent_flag (from InteractionCallCenter), session_duration_seconds (from InteractionDigital), acquisition_channel (from InteractionDigital), drop_off_step (from InteractionDigital), mail_piece_type (from InteractionDirectMail), response_type (from InteractionDirectMail), undeliverable_flag (from InteractionDirectMail), campaign_id, policy_status

**Uses:** Journey pattern clustering (sequence of interaction types preceding lapse or conversion), touchpoint attribution, interaction gap analysis, next-best-action model training, cross-channel cohort comparisons

---

## Data Gaps and Proxy Strategy

Given the constraint of no psychographic data, use the following proxies.

| Missing Data | Available Proxy | Source | Accuracy |
|-------------|----------------|--------|----------|
| Income | Zip code median household income | U.S. Census / ACS | ±25%; use quintiles, not exact |
| Income | Annual premium / face amount ratio | Policy | Relative affordability proxy |
| Financial stress | NSF rate, payment method downgrades, chronic late payments | PaymentSummary | High behavioral validity |
| Health status | Age, tobacco flag, underwriting class | Application + Policy | Limited; simplified issue restricts data |
| Household composition | Beneficiary relationship, marital status, spouse application linkage | Beneficiary + Person + Application | Good; spouse application data directly captures joint household intent |
| Conversion intent | Near-term-expiry flag on term policies, call center topics, coverage question calls | Policy + InteractionCallCenter | Moderate; requires NLP on call transcripts to surface conversion intent language |
| Life stage | Issue age band + product type + face amount | Policy | Strong proxy |
| Digital sophistication | Acquisition channel, device type, session behavior | InteractionDigital | Behavioral signal |
| Brand engagement | Call reason mix, coverage question calls, reinstatement behavior | InteractionCallCenter | Indirect engagement signal |
| Price sensitivity | Payment method (check vs. EFT), face amount relative to age-band average | Policy | Behavioral proxy |
| Motivations (JTBD) | Call center topic tags, NLP on call transcripts, cancellation reasons | InteractionCallCenter | Requires NLP investment; high value |

---

## Data Quality Priorities

Given the stated data sources (application, policy, payment history, call center logs), prioritize data quality investment in this order:

| Priority | Entity | Key Risk | Remediation |
|----------|--------|---------|-------------|
| 1 | Payment | Inconsistent return_reason_code taxonomy across payment processors | Standardize codes; map historical to canonical set |
| 2 | InteractionCallCenter | call_reason_primary over-use of "Other"; low-quality tagging | Re-tag sample using NLP; retrain categorization model |
| 3 | LapseEvent | lapse_reason_code often defaults to NonPayment even for voluntary surrenders | Enrich with call center data: any cancellation_intent call before lapse |
| 4 | Application | campaign_id not populated for all digital applications; attribution gaps | Implement UTM capture → campaign_id mapping at application submission |
| 5 | AffinityMember | Person-to-member match rate below 100%; unmatched members missed for analysis | Run probabilistic matching on name + zip + DOB; target >90% match rate |
| 6 | InteractionDigital | Anonymous sessions not linked to Person after application | Stitch session_id → application_id → person_id at application submission |
| 7 | PolicyChange | face_amount_delta may not be captured if only the new amount is stored; no prior amount recorded | Require both prior and new face amount fields at change event; backfill from policy history |
| 8 | PolicyConversion | conversion_trigger often left as Unknown; attribution to campaigns is incomplete | Link outbound campaign activity in the 90 days prior to conversion date to assign campaign_id |
| 9 | PolicyRider | rider_add_date missing for riders issued at policy origination (treated as null); inconsistent | Default add_date = policy effective_date and add_channel = AtIssue for all riders present at issue |
| 10 | Application (spouse) | linked_application_id and household_link_id not always populated when spouse applies by phone | Require CSR to link applications at time of entry; audit household linkage completeness monthly |
| 11 | CustomerInteraction | Hub records not created retroactively for historical data; InteractionCallCenter and InteractionDigital records predating hub launch will have null customer_interaction_id | Back-fill customer_interaction_id on detail records where a deterministic match exists; treat null as a data maturity flag, not a missing interaction; report linkage rate monthly |
| 12 | InteractionDirectMail | tracking_code / offer_code not captured consistently on inbound responses processed by phone or web; attribution gaps for mail-sourced applications | Enforce offer_code capture as required field on phone intake and web landing pages used in mail campaigns; audit quarterly |

---

## Notes on Regulatory and Privacy Constraints

| Constraint | Impact on Data Model |
|-----------|---------------------|
| State insurance regulations | Some states restrict use of certain data in pricing/segmentation; flag issue_state on every policy |
| FCRA | If using credit bureau or third-party financial data for segmentation, adverse action rules apply |
| GLBA / state privacy laws | Customer data sharing with affinity partners requires contractual controls; track data_sharing_consent on Person |
| CAN-SPAM / TCPA | email_opt_in_flag and sms_opt_in_flag must be enforced at campaign targeting layer, not just captured |
| Do Not Call registry | do_not_contact_flag must be checked against DNC list before outbound phone campaigns |
| HIPAA | Simplified issue health questions (tobacco use) may be subject to state-level health data protections; consult compliance |
