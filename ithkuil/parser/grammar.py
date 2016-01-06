grammar = """
// ------------------ kinds of words ----------------------

word <- verbal_adjunct
      / personal_adjunct
      / aspectual_adjunct
      / affixual_adjunct
      / bias_adjunct
      / formative;

// ------------------ some basic definitions --------------------

tone <- "\\" / "_" / "/" / "ˇ" / "^" / "¯";

consonant4 <- "hw" / "w" / "y" / "h";

consonant <- "c’" / "cʰ" / "č’" / "čʰ" / "dh" / "k’" / "kʰ" / "p’" / "pʰ"
           / "q’" / "qʰ" / "t’" / "tʰ" / "xh"
           / "b" / "c" / "č" / "ç" / "d" / "f" / "g" / "h" / "j"
           / "k" / "l" / "ļ" / "m" / "n" / "ň" / "p" / "q"
           / "r" / "ř" / "s" / "š" / "t" / "ţ" / "v" / "w" / "x" / "y" / "z"
           / "ż" / "ž";

consonants <- consonant+;

geminable <- "l" / "m" / "n" / "ň" / "r";

vowel <- "a" / "e" / "i" / "o" / "u"
       / "â" / "ê" / "î" / "ô" / "û"
       / "ë" / "ö" / "ü"
       / "à" / "è" / "ì" / "ò" / "ù"
       / "á" / "é" / "í" / "ó" / "ú";

bare_vowel <- "a" / "e" / "i" / "o" / "u";

unmarked_vowel <- "a" / "e" / "i" / "o" / "u"
                / "â" / "ê" / "î" / "ô" / "û"
                / "ë" / "ö" / "ü";

decorated_vowel <- "â" / "ê" / "î" / "ô" / "û"
                 / "ë" / "ö" / "ü";

stressed_vowel <- "á" / "é" / "í" / "ó" / "ú"
                / "ëë" / "öö" / "üü"
                / "ââ" / "êê" / "îî" / "ôô" / "ûû";

grave_vowel <- "à" / "è" / "ì" / "ò" / "ù";

not_diphthong <- "aù" / "eù" / "iù" / "où" / "öù" / "ëù"
               / "aì" / "eì" / "oì" / "uì" / "öì" / "ëì";

diphthong <- "au" / "eu" / "iu" / "ou" / "öu" / "ëu"
           / "ai" / "ei" / "oi" / "ui" / "öi" / "ëi"
           / "áu" / "éu" / "íu" / "óu"
           / "ái" / "éi" / "ói" / "úi"
           / "àu" / "èu" / "ìu" / "òu"
           / "ài" / "èi" / "òi" / "ùi";

bare_diphthong <- "au" / "eu" / "iu" / "ou"
                / "ai" / "ei" / "oi" / "ui";

unmarked_diphthong <- "au" / "eu" / "iu" / "ou" / "öu" / "ëu"
                    / "ai" / "ei" / "oi" / "ui" / "öi" / "ëi";

stressed_diphthong <- "áu" / "éu" / "íu" / "óu"
                    / "ái" / "éi" / "ói" / "úi"
                    / "ööu" / "ëëu" / "ööi" / "ëëi";

grave_diphthong <- "àu" / "èu" / "ìu" / "òu"
                 / "ài" / "èi" / "òi" / "ùi";

// this bypasses the problem of syllabic geminates - to be discussed
sep <- stop? (consonant / '-') * stop?;  // vowel separator

syllable <- sep (diphthong / vowel);

bare_syllable <- sep (bare_diphthong / bare_vowel);

unmarked_syllable <- sep (unmarked_diphthong / not_diphthong / unmarked_vowel);

decorated_syllable <-  sep ("öu" / "ëu" / "öi" / "ëi" / decorated_vowel);

stressed_syllable <- sep (stressed_diphthong / stressed_vowel);

double_syllable <- sep ("ëë" / "öö" / "üü"
                 / "ââ" / "êê" / "îî" / "ôô" / "ûû"
                 / "ööu" / "ëëu" / "ööi" / "ëëi");

grave_syllable <- sep (grave_diphthong / grave_vowel);

unstressed_syllable <- !stressed_syllable syllable;

vowels <- (vowel vowel / vowel) !vowel;

stop <- "’";

// ------------------- stress ------------------------------------

penultimate_stress <- unmarked_syllable* sep !syllable;

ultimate_stress <- stressed_syllable sep !syllable
                 / grave_syllable decorated_syllable sep !syllable
                 / grave_syllable decorated_syllable decorated_syllable sep !syllable
                 / decorated_syllable decorated_syllable double_syllable sep !syllable
                 / decorated_syllable double_syllable sep !syllable
                 / unmarked_syllable ultimate_stress;

antepenultimate_stress <- stressed_syllable unmarked_syllable unmarked_syllable sep !syllable
                        / sep stressed_vowel grave_vowel unmarked_syllable sep !syllable
                        / decorated_syllable grave_syllable bare_syllable sep !syllable
                        / decorated_syllable decorated_syllable grave_syllable sep !syllable
                        / double_syllable bare_syllable decorated_syllable sep !syllable
                        / unmarked_syllable antepenultimate_stress;

preantepenultimate_stress <- stressed_syllable unmarked_syllable unmarked_syllable unmarked_syllable sep !syllable
                           / sep stressed_vowel grave_vowel unmarked_syllable unmarked_syllable sep !syllable
                           / decorated_syllable grave_syllable unmarked_syllable bare_syllable sep !syllable
                           / double_syllable decorated_syllable unmarked_syllable unmarked_syllable sep !syllable
                           / unmarked_syllable preantepenultimate_stress;

// ------------------- formative parsing -------------------------

formative <- tone? stress_formative bias?;

stress_formative <- penultimate_stress_formative
                  / ultimate_stress_formative
                  / antepenultimate_stress_formative
                  / preantepenultimate_stress_formative;

penultimate_stress_formative <- &penultimate_stress main_formative;

ultimate_stress_formative <- &ultimate_stress main_formative;

antepenultimate_stress_formative <- &antepenultimate_stress main_formative;

preantepenultimate_stress_formative <- &preantepenultimate_stress main_formative;

main_formative <- (prefix? vr stop?)? incorporated_root root_part has_format
                / (prefix? vr stop?)? incorporated_root root_part_we has_format
                / prefix_no_cv_vl? vr stop cv vl root_part suffixes vf_no_format?
                / (prefix? vr)? root_part suffixes vf_no_format?;

prefix <- (cv? vl)? cs / vl? cg;
prefix_no_cv_vl <- cs / cg;

cv <- consonants;

vl <- vowels;

cs <- geminable "-" geminable consonant*;

cg <- validation;

vr <- vowels;

root_part <- root vc civi? ca;
root_part_we <- root vc "wë" ca;

root <- !validation consonants;

vc <- vowels stop vowels
    / vowels stop
    / vowels;

civi <- consonant4 vowel;

ca <- consonants;

has_format <- suffixes_fe vf? / suffix* vf_format;

suffix <- vowels !suffix_fe_type consonants;

suffixes <- suffix*;

suffix_format_exp <- vowels suffix_fe_type;

suffixes_fe <- suffix* suffix_format_exp suffix*;

suffix_fe_type <- ("tt" / "pk" / "qq" / "tk"
                / "st’" / "sp’" / "sq’" / "sk’"
                / "št’" / "šp’" / "šq’" / "šk’") !consonant;

vf_no_format <- ("a" / "i" / "e" / "u") !vowel;
vf <- vowels;
vf_format <- !vf_no_format vf;

incorporated_root <- root vowels;

validation <- ("hw" / "hr" / "hh" / "hn" / "hm"
             / "lw" / "ly" / "rw" / "ry"
             / "řw" / "řy"
             / "w" / "y" / "h") !consonant;

bias <- stop consonant consonant
      / stop consonant;

// ----------------------------- other ------------------------------------

// dummy

verbal_adjunct <- "verbal";
personal_adjunct <- "personal";
aspectual_adjunct <- "aspectual";
affixual_adjunct <- "affixual";
bias_adjunct <- "bias";
"""