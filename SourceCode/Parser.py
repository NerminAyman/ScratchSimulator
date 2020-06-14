#!/usr/bin/env python
# coding: utf-8
# %%


import json
import webcolors
import colorsys
import sys


# %%


# with open('project1Part2.json') as json_file:
#     data = json.load(json_file)
#with open('afterblocks.json') as json_file:
  #  data = json.load(json_file)
##with open('VisualProgramming/project.json') as json_file:
 #   data1 = json.load(json_file)
# with open('test1.json') as json_file1:
#      data3 = json.load(json_file1)  
# with open('project.json') as json_file1:
#     data2 = json.load(json_file1)  
with open(sys.argv[1]) as json_file1:
    data2 = json.load(json_file1)
    
    


# %%


def getKey(key):    
        if(key=="down arrow"):
            key="down"
        elif(key=="up arrow"):
            key="up"
        elif(key=="right arrow"):
            key="right"
        elif(key=="left arrow"):
            key="left"
        return key
def getparent(state,z):
    while(True):
            if(state['parent'] is None):
                return "nothing"
            if(z[state['parent']]['opcode']=="control_repeat" and state==z[z[state['parent']]['inputs']['SUBSTACK'][1]]):
                    return "endRepeat"
            elif(z[state['parent']]['opcode']=="control_if_else"):
                    if(state==z[z[state['parent']]['inputs']['SUBSTACK2'][1]]): 
                         return "endElse"
                    elif(state==z[z[state['parent']]['inputs']['SUBSTACK'][1]]):
                         return "endThen"
            elif(z[state['parent']]['opcode']=="control_if"):
                if(state==z[z[state['parent']]['inputs']['SUBSTACK'][1]]):
                         return "endThen"
                    
            state=z[state['parent']]
def opcodeParsing(state,s,z,nextelse):
    
            if(state['next'] is None):
                state2=state
                z2=z
                temp=getparent(state2,z2)
                if(temp!="nothing"):
                        nextelse.append(temp)
                    
            if(state['opcode']==  "event_whenflagclicked"):
                s+="if GREENFLAG then "      
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
            if(state['opcode']==  "event_whenkeypressed"):
                key=state['fields']['KEY_OPTION'][0]                
                s+="if KeyPressed "+getKey(key)+" then "
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="control_repeat") :
                s+="Repeat"+" "
                s=getInputs(state,s,z)
                                      
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                if('SUBSTACK' in state['inputs'] ):
                    nextelse.append(state['inputs']['SUBSTACK'][1])
                   
            elif (state['opcode']=="motion_movesteps") :
                s+="Move"+" "
                s=getInputs(state,s,z)
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_turnright") :
                s+="Turn Right"+" "
                s=getInputs(state,s,z) 
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_turnleft") :
                s+="Turn Left"+" "
                s=getInputs(state,s,z) 
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                
            elif (state['opcode']=="motion_pointindirection") :
                s+="Point"+" "
                s=getInputs(state,s,z) 
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_gotoxy") :
                if(isinstance(state['inputs']['X'][1],str)) :
                    x=z[state['inputs']['X'][1]]['opcode'].split('_')[1] 
                else:
                    x=state['inputs']['X'][1][1]
                if(isinstance(state['inputs']['Y'][1],str)) : 
                    y=z[state['inputs']['Y'][1]]['opcode'].split('_')[1] 
                else:
                    y=state['inputs']['Y'][1][1]
                                 
                s+="GoTo "+x+" "+y+" "
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_setx") :  
                s+="SetX "
                s=getInputs(state,s,z)              
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_sety") :  
                s+="SetY "
                s=getInputs(state,s,z)              
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_changexby") :  
                s+="ChangeXBy "
                s=getInputs(state,s,z)              
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                    
            elif (state['opcode']=="motion_changeyby") :  
                s+="ChangeYBy "
                s=getInputs(state,s,z)              
                if(state['next']!=None):                    
                    nextelse.append(state['next'])
                
#             elif (state['opcode']=="control_wait") :
#                 s+="wait "+" "
#                 s=getInputs(state,s) 
#                 nextif=state['next']
                
#             elif (state['opcode']=="data_setvariableto") :
#                 s+=state['fields']['VARIABLE'][0]+"="
#                 s=getInputs(state,s) 
#                 nextif=state['next']
                
            elif("control_if" in state['opcode']):
                s+="if"+" "
                no_condition=False
                if(not state['inputs']):
                    return s, nextelse
                if(state['next']!=None):                    
                    nextelse.append(state['next'])

                if(state['opcode']=="control_if_else"): 
                    if('SUBSTACK2' in state['inputs'] ):                        
                        nextelse.append(state['inputs']['SUBSTACK2'][1])
                    nextelse.append("else")
                if('SUBSTACK' in state['inputs'] ):
                    nextelse.append(state['inputs']['SUBSTACK'][1])
                    

                if('CONDITION' in state['inputs'] ):
                    condition=state['inputs']['CONDITION'][1]
                    condition=z[condition]
                else:
                    return s,nextelse
                
             
                if("operator" in condition['opcode']):
                    if(isinstance(condition['inputs']['OPERAND1'][1],str)):                       
                        s1= z[condition['inputs']['OPERAND1'][1]]['opcode'].split('_')[1]
                    else:
                        s1= condition['inputs']['OPERAND1'][1][1]
                    if(isinstance(condition['inputs']['OPERAND2'][1],str)):  
                        s2=z[condition['inputs']['OPERAND2'][1]]['opcode'].split('_')[1] +" then "
                    else:
                        s2=condition['inputs']['OPERAND2'][1][1]+" then "
                       
                if(condition['opcode']=="operator_equals"):
                    s+= s1+ "==" +s2
                elif(condition['opcode']=="operator_gt"):
                    s+= s1+ ">" +s2                   
                elif(condition['opcode']=="operator_lt"):
                    s+= s1+ "<" +s2
                       
#                 elif(condition['opcode']=="sensing_mousedown"):
#                     s+= "(mouse Down) then "
                elif(condition['opcode']=="sensing_keypressed"):
                    keyPressedOpcode=condition['inputs']['KEY_OPTION'][1]
                    
                    keyPressed=z[keyPressedOpcode]['fields']['KEY_OPTION'][0]
                    s+= "Key\""+ getKey(keyPressed) + "\"ispressed then " 
                    
                elif(condition['opcode']=="sensing_touchingcolor"):
                    color=condition['inputs']['COLOR'][1][1]
                    s+= "Color\""+color[1:]+ "\"istouched then " 
                    

                
            
          
            return s,nextelse    
    
def getInputs(state,s,z):           
        if(state['inputs'] != None):
            inputs=state['inputs']
            i=0
            for state1 in inputs.values():
                if(i==0):
                    try:
                        val = int(state1[1][1])
                        s+=state1[1][1]+" "
                    except ValueError:
                        addr=state1[1]
                        opcode=z[addr]["opcode"]
                        if(opcode=="sensing_mousex"):
                              s+="mousex "
                        elif(opcode=="sensing_mousey"):
                              s+="mousey "
                        elif(opcode=="motion_xposition"):
                              s+="xposition "
                        elif(opcode=="motion_yposition"):
                              s+="yposition "          

                i+=1    
                     
        return s

def parseJson(dataDict,outputfile):
    x=dataDict['targets']
    y=x[1]
    z=y['blocks']
    output=""
    nextelse=[]
    i=0
    s=[]
    for state in z.values(): 
        if(state['parent'] is None):
            nextelse.append([])
            s.append("")
            s[i],nextelse[i]=opcodeParsing(state,s[i],z,nextelse[i])
            i+=1           
    while(nextelse):
        first_stack=nextelse.pop()
        s1=s.pop()             
        while(first_stack):
            nextif=first_stack.pop() 
           
            if(nextif=="else" or nextif=="end" or nextif=="endThen" or nextif=="endElse" or nextif=="endRepeat"): 
                s1+=nextif+" "
                
            else:
                s1,first_stack= opcodeParsing(z[nextif],s1,z,first_stack)
#             print(s1)
#         s1+="end_of_this_program "
        output=s1+output
    output="OUT = "+output
    print(output)
        


    with open(outputfile,'w') as f:
        f.write(output)
        f.write("\n")


# %%


parseJson(data2,'output.txt')


# %%





# %%




