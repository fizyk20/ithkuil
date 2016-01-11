from arpeggio import PTNodeVisitor

def pass_visitor(num=0):
    '''A visiting function that will pass the selected child unchanged
    (by default: the first one)'''
    def visitor(a, node, children):
        return children[num]
    return visitor

def collect_visitor(a, node, children):
    '''A visiting function that joins all children into one string'''
    return ''.join(children)

def constant_visitor(const):
    '''A visiting function that returns a constant'''
    def visitor(a, node, children):
        return const
    return visitor

def constant_add_visitor(const, num=0):
    '''A visiting function that extends one of the child dicts with a constant dict'''
    def visitor(a, node, children):
        children[num].update(const)
        return children[num]
    return visitor
    
def dict_visitor(key):
    '''A visiting function that joins the children into a string and returns it as a value in a dict'''
    def visitor(a, node, children):
        return { key: ''.join(children) }
    return visitor

def dict_combine_visitor(a, node, children):
    '''A visiting function that combines child dicts into one'''
    result = {}
    for child in children:
        if isinstance(child, dict): result.update(child)
    return result

def dict_append_visitor(to_append):
    '''A visiting function that combines child dicts into one and extends it'''
    def visitor(a, node, children):
        result = dict_combine_visitor(a, node, children)
        result.update(to_append)
        return result
    return visitor

class IthkuilVisitor(PTNodeVisitor):
    ''' A visitor class that generates a dict of all slots present in the word with some additional info'''

    # do nothing with a recognized word, the dict is already generated
    visit_word = pass_visitor()
    
    ### Formatives

    # do nothing with single consonants
    visit_consonant = pass_visitor()

    # do nothing with single vowels
    visit_vowel = pass_visitor()

    # combine consonant blocks
    visit_consonants = collect_visitor

    # combine vocalic blocks
    visit_vowels = collect_visitor

    # do nothing with "geminable" consonants
    visit_geminable = pass_visitor()

    # do nothing with consonants belonging to the set of four
    visit_consonant4 = pass_visitor()

    # tone goes directly into the dict as a slot
    visit_tone = dict_visitor('tone')

    # for a glottal stop just return the character
    def visit_stop(self, node, children): return '’'

    # add Cv slot to the dict
    visit_cv = dict_visitor('Cv')

    # add Vl slot to the dict
    visit_vl = dict_visitor('Vl')

    # '-' gets lost in parsing - reinsert it and add Cs slot to the dict 
    def visit_cs(self, node, children):
        children.insert(1, '-')
        return dict_visitor('Cs')(self, node, children)

    # do nothing with the recognized valid consonantal form
    visit_validation = pass_visitor()

    # add Cg slot to the dict
    visit_cg = dict_visitor('Cg')

    # combine the optional prefix into a single dict
    visit_prefix = dict_combine_visitor
    visit_prefix_no_cv_vl = dict_combine_visitor

    # add Vr slot to the dict
    visit_vr = dict_visitor('Vr')

    # root goes into the Cr slot
    visit_root = dict_visitor('Cr')

    # incorporated root uses the rule for root - so it gets the root as Cr slot -> redefine to Cx and add Vp
    def visit_incorporated_root(self, node, children): return { 'Cx': children[0]['Cr'], 'Vp': children[1] }

    # add Vc slot
    visit_vc = dict_visitor('Vc')

    # add Ci+Vi slot
    visit_civi = dict_visitor('Ci+Vi')

    # add Ca slot
    visit_ca = dict_visitor('Ca')

    # both Vf and Vf without format belong to the Vf slot
    visit_vf_no_format = dict_visitor('Vf')
    visit_vf = dict_visitor('Vf')

    # Vf with format uses another rule, so the dict is already created - do nothing
    visit_vf_format = pass_visitor()

    # deal with a single suffix - create a dict with the type and degree
    def visit_suffix_format_exp(self, node, children): return { 'type': children[1], 'degree': children[0] }
    def visit_suffix(self, node, children): return { 'type': children[1], 'degree': children[0] }
    
    # do nothing with the recognized format expansion suffix - other rules will take care of it
    visit_suffix_fe_type = pass_visitor()
    
    # combine a list of suffixes into a list in the VxC slot
    def visit_suffixes(self, node, children): return { 'VxC': children }
    def visit_suffixes_fe(self, node, children): return { 'VxC': children }

    # combine all the parts that define the format into a single dict
    visit_has_format = dict_combine_visitor

    # combine the central part of the formative
    visit_root_part_we = dict_combine_visitor
    visit_root_part = dict_combine_visitor

    # combine everything except tone and bias
    visit_main_formative = dict_combine_visitor

    # stress recognition - add an appropriate key to the dict
    visit_penultimate_stress_formative = constant_add_visitor({ 'stress': -2 })
    visit_ultimate_stress_formative = constant_add_visitor({ 'stress': -1 })
    visit_antepenultimate_stress_formative = constant_add_visitor({ 'stress': -3 })
    visit_preantepenultimate_stress_formative = constant_add_visitor({ 'stress': -4 })

    # the stress is already recognized - do nothing
    visit_stress_formative = pass_visitor()
    
    # recognize intensified bias
    def visit_cb(self, node, children):
        block = ''.join(children)
        cb = ""
        plus = False
        if len(block) == 2 and block[0] == block[1]:
            cb = block[0:1]
            plus = True
        elif len(block) == 3 and block[0] == block[1]:
            cb = block[1:]
            plus = True
        elif len(block) == 3 and block[1] == block[2]:
            cb = block[0:2]
            plus = True
        else:
            cb = block
        return { 'Cb': cb, 'Cb+': plus }

    # omit the glottal stop when passing the bias part
    visit_bias = pass_visitor(1)
    
    # append word type information to a recognized formative
    visit_formative = dict_append_visitor({ 'type': 'formative' })
    
    ### vebal adjuncts
    
    # add Cl slot to the dict
    visit_cl = dict_visitor('Cl')
    
    # add Vs slot to the dict
    visit_vs = dict_visitor('Vs')
    
    # add Ve slot to the dict
    visit_ve = dict_visitor('Ve')
    
    # add Vm slot to the dict
    visit_vm = dict_visitor('Vm')
    
    # append word type information
    visit_verbal_adjunct = dict_append_visitor({ 'type': 'verbal adjunct' })
    
    ### personal adjuncts
    
    # add C1 slot to the dict
    visit_c1 = dict_visitor('C1')
    
    # collect the case slot vowels
    visit_vcp = collect_visitor
    
    # add Vc slot to the dict
    visit_vcp1 = dict_visitor('Vc')
    
    # add Vc2 slot to the dict
    visit_vcp2 = dict_visitor('Vc2')
    
    # add Cz slot
    visit_cz = dict_visitor('Cz')
    
    # add Vz slot
    visit_vz = dict_visitor('Vz')
    
    # collect suffix consonants
    visit_csp = collect_visitor
    
    # collect suffix vowels
    visit_vsp = collect_visitor
    
    # combine slots into suffix info
    def visit_rev_suffix(self, node, children):
        return { 'type': children[0], 'degree': children[1] }
    
    # collect all suffixes
    def visit_rev_suffixes(self, node, children):
        return { 'VxC': children }
    
    # collect recognized short form information
    visit_short_form = dict_combine_visitor
    
    # collect recognized long form information
    visit_long_form = dict_combine_visitor
    
    # collect recognized conjunct form information
    def visit_conjunct_form(self, node, children):
        if len(children) == 2:
            if 'VxC' in children[1]:
                children[1]['VxC'].append(children[0])
            else:
                children[1]['VxC'] = [children[0]]
            return children[1]
        else:
            return children[0]             
    
    # collect recognized collapsed form information
    visit_collapsed_form = dict_combine_visitor
    
    # collect single referent adjunct info
    visit_single_referent = dict_combine_visitor
    
    # recognize stress
    visit_single_referent_penultimate = constant_add_visitor({ 'stress': -2 })  
    visit_single_referent_ultimate = constant_add_visitor({ 'stress': -1 })
    
    # add tone slot
    visit_high_tone = dict_visitor('tone') 
    visit_four_tone = dict_visitor('tone')  
    visit_four_tone_single = dict_visitor('tone')
    
    # add Vw slot to the dict
    visit_vw = dict_visitor('Vw')
    
    # add Ck slot to the dict
    visit_ck = dict_visitor('Ck')
    
    # add C2 slot to the dict
    visit_c2 = dict_visitor('C2')
    
    # collect dual referent adjunct info
    visit_dual_referent = dict_combine_visitor
    
    # recognize stress
    visit_dual_referent_penultimate = constant_add_visitor({ 'stress' : -2 }) 
    visit_dual_referent_ultimate = constant_add_visitor({ 'stress' : -1 })
    visit_dual_referent_antepenultimate = constant_add_visitor({ 'stress' : -3 })
    visit_dual_referent_preantepenultimate = constant_add_visitor({ 'stress' : -4 })
    
    # add word type info
    visit_personal_adjunct = constant_add_visitor({ 'type': 'personal adjunct' })
    
    # handle aspectual adjuncts
    def visit_aspectual_adjunct(self, node, children):
        return { 'type': 'aspectual adjunct', 'Vs': ''.join(children) }
    
    # handle affixual adjuncts
    def visit_affixual_adjunct(self, node, children):
        return { 'type': 'affixual adjunct', 'VxC': { 'type': children[1], 'degree': ''.join(children[:-1]) } }
    
    # handle bias adjuncts
    visit_bias_adjunct = dict_append_visitor({ 'type': 'bias adjunct' })
