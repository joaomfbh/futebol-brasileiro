import pandas as pd
import functions
import re

try:
    def internacional_gather():

        with open('offline_pages/internacional_27072020.html', 'rb') as file:
            pagina = file.read()
        
        # Url from Internacional conquests page
        content = functions.webpage_requests('https://internacional.com.br/historia/titulos')
        soup = content[1]

        if len(pagina) == content[0]:
            # Conquests are in a table, tr elements
            lst_conquests = []

            for i in soup.table.find_all('tr')[1:]: 
                lst_conquests.append({'titulo':str(i.td.contents[1]),
                                      'ano_conquista':str(i.td.contents[0])})

            # Transform the list of dictionaries 'lst_conquests' in a dataframe
            df = pd.DataFrame(lst_conquests)

            '''
            Quality and structure issues:
            1. The conquest 'Campeão Metropolitano de Porto Alegre' has many years in the same row.
            2. Remove the dash (-) in conquest names
            3. Remove the unicode character \xa0 (non-breaking space)
            4. Remove HTML code in year of conquests
            5. The math prefixes (bi, tri, tetra, etc) and some words lik ('Campeao do', 'Campeão da', 'Campeão invicto') must be removed to show the real name of conquest
            6. In some cases, appear the locate where the championship was disputed and this information must be removed too.
            7. Duplicated in conquest 'Copa da Governador do Estado' because appear two rows for the same year.
            '''
    
            # 1. The conquest 'Campeão Metropolitano de Porto Alegre' has many years in the same row.
            camp_metrop = df.loc[1,'titulo']

            # The pattern get only numbers
            pattern = re.compile(r"(\d+)")
            camp_metrop_anos = re.findall(pattern, camp_metrop)

            lst_camp_metrop = []
            # Create a row for each year and store in a list to after attach in dataframe
            for i in camp_metrop_anos:
                lst_camp_metrop.append({'titulo':'Campeão Metropolitano de Porto Alegre',
                                        'ano_conquista':int(i)})
    
            # Exlcude this row becauase the content has in lst_camp_metrop
            df.drop(index=1, inplace=True)

            # Make a copy of original df
            df_clean = df.copy()

            # 2. Remove the dash (-) in conquest names
            df_clean['titulo'] = df_clean.loc[:,'titulo'].str.replace('–','')

            # 3. Remove the unicode character \xa0 (non-breaking space)
            df_clean['titulo'] = df_clean.loc[:,'titulo'].str.replace(u'\xa0',u'')

            # 4. Remove HTML code in year of conquests and convert to int
            df_clean['ano_conquista'] = df_clean.loc[:,'ano_conquista'].str.extract(r'(\d+)').astype(int)

            # Append 'Campeão Metropolitano de Porto Alegre' to df_clean
            df_clean = df_clean.append(lst_camp_metrop, ignore_index=True)
            df_clean.reset_index(drop=True, inplace=True)

            # 5. The math prefixes (bi, tri, tetra, etc) and some words lik ('Campeao do', 'Campeão da', 'Campeão invicto') must be removed to show the real name of conquest
            df_clean.loc[:,'titulo'] = functions.remove_math_prefixes(df_clean, 'titulo')
            df_clean.loc[:,'titulo'] = df_clean.loc[:,'titulo'].str.strip()

            # Needed to convert the first letter of these cases to uppercase
            for i,j in enumerate(df_clean['titulo'].values):
                if j[0].islower():
                    df_clean.loc[i,'titulo'] = j[0].upper() + j[1:]

            for i,j in enumerate(df_clean['titulo'].values):
                nomes_replace = ['Campeão da','Campeão de','Campeão do','de forma invicta','invicto','Campeão invicto da']
                for k in nomes_replace:
                    if k in j:
                        df_clean.loc[i,'titulo'] = df_clean.loc[i,'titulo'].replace(k,'').strip()

            for i,j in enumerate(df_clean['titulo'].values):
                nomes_replace = ['Campeão ']
                for k in nomes_replace:
                    if k in j:
                        df_clean.loc[i,'titulo'] = df_clean.loc[i,'titulo'].replace(k,'Campeonato ').strip()

            # 6. In some cases, appear the locate where the championship was disputed and this information must be removed too.
            df_clean.loc[:,'titulo'] = df_clean['titulo'].apply(lambda x: x.split(',')[0])

            # 7. Duplicated in conquest 'Copa da Governador do Estado' because appear two rows for the same year.
            df_clean.drop(df_clean[df_clean.titulo == 'Copa da Governador do Estado'].index, inplace=True)
            df_clean.reset_index(drop=True, inplace=True)
    
            functions.save_to_csv(df_clean, 'internacional')

            return df_clean
        else:
            raise Exception("The webpage changed and code must be reviewed.")

except Exception as e:
    print(e)


internacional_gather()