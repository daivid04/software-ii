import { createClient } from 'https://esm.sh/@supabase/supabase-js';

export const URL_STORE = "https://faxgvryumrbseucrcumv.supabase.co";
export const ANON_KEY = "sb_publishable_Af0m-z4RJzwZ4Nn4bqeVrg_XfA-oipJ";

export const SUPABASE = createClient(URL_STORE, ANON_KEY);