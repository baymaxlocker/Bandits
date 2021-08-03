# -*- coding: utf-8 -*-
"""

Author: Manny Torres
"""


#from Tests import openFile
import csv, random
import math

class Bandit(object):
	

	
	def main(self):		

		file = 'BanditsData_test.csv'

	# Static Variables
		self.expRate = 0.3
		self.distParam = 0.1
		self.decay = 0.6
		self.rewardWeight = 0.9
		
	# Results	
		self.probabilities={}
		self.cumulative_reward={}
		self.norm_weight={}
	
	# Run the calculations
		self.openfile(file)
		#bandit = BanditSet(5,{'SA':0, 'SB':0, 'SC':0, 'SD':0}, self.expRate, self.distParam, self.decay, self.rewardWeight)


		
	
	def openfile(self,file):
		
		with open(file, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			firstrow = next(reader)

			# Setting all starting values
			self.probabilities, self.norm_weight, self.cumulative_reward = self.startingGrid(firstrow)
		

			for row in reader:
				random_arm = self.pickArmIndex(self.cumulative_reward)
				arm_value = row[random_arm]
				print("\nSelected arm is "+random_arm+" with a value of "+str(arm_value)+"\n")
				# Update weights : calculate weight and normalized weight
				self.updateWeight(random_arm, self.norm_weight, arm_value)
				# Update probability : calculate probability and normalized probability
				self.updateProbability(random_arm, self.norm_weight, self.probabilities)
				# Update reward
				self.reward_memory(arm_value, random_arm, self.cumulative_reward)

		

	# Prepare all starting values: Starting Probabilities for all arms. Starting Weight for all arms. Starting cumulative rewards for all arms.
	def startingGrid(self, banditRow):

		# Use 3 dictionaries: one for the updated probabilities, another for the updated normalized weight and another for the cumulative reward
		
		probabilities, normWeight = self.calc_startprob(banditRow)
		cumulative_reward = {'Sample A cumulative reward':0,'Sample B cumulative reward':0,'Sample C cumulative reward':0,'Sample D cumulative reward':0}
		
		print("Starting probabilities: "+str(probabilities))
		print("Starting weights: "+ str(normWeight))
		print("Starting cumulative rewards: "+ str(cumulative_reward)+"\n")

		return probabilities, normWeight, cumulative_reward


	# Takes cumulative reward Dictionary as input and returns selected arm to play
	# If all arms have the same cumulative reward, it will pick one randomly.
	# If not, it will pick one randomly giving a higher chance per weighted probability
	# Returns a the arm name, for example "Sample A" or "Sample B"
	
	def pickArmIndex(self, cumulativeRewards):
		
		equal = True 
	
		print("\n\nSelecting arm for next iteration")
		# extracting value to compare
		val = list(cumulativeRewards.items())
		
		for value in range (len(val)):
			
			if val[value][1] != val[value-1][1]:
		
				equal = False 

		if equal == True:
			print("values are all the same")
			arm = random.choice(val)
			arm_index = arm[0]

		elif equal == False:
			print("found diff value")
			#val.sort(key=lambda x:x[1], reverse=True)
			#print("Sorted list "+str(val))
			arm = random.choices(val,weights=[val[0][1], val[1][1], val[2][1], val[3][1]])
			arm_index = arm[0][0]

		
		converted_index = self.convention_converter(arm_index)
		
		return converted_index



	def calc_startprob(self,banditRow):

		startProb = 1 / float(len(banditRow))
		self.probabilities = {'Sample A prob':0, 'Sample B prob':0, 'Sample C prob':0, 'Sample D prob':0}
		self.norm_weight = {'Sample A norm weight':0, 'Sample B norm weight':0, 'Sample C norm weight':0, 'Sample D norm weight':0}

		for i,value in self.probabilities.items():
			self.probabilities[i] = startProb
		
		for j,value in self.norm_weight.items():
			self.norm_weight[j] = startProb

		return self.probabilities, self.norm_weight


	# Returns a dictionary with normalized weights and updates the overall normilized weights.
	def updateWeight(self, index, normweights, reward):
		"""
		Update the weight for the chosen index using 
		the parameters.
		"""
		print("Working on weights...")
		for i in normweights:
			if i.startswith(index): 
				key = i

		weight = normweights[key]
		updatedWeight = self.decay * weight + self.rewardWeight * int(reward)
		normweights[key] = updatedWeight
		print("updated weights are: "+str(normweights))
		print("Normalizing weights...")
		allweights_sum = sum(normweights.values())
		for w,value in normweights.items():
			normweights[w] = value/allweights_sum
		self.norm_weight = normweights
		print("Normalized weights updated.")
		print("Normalized weights: "+str(self.norm_weight))
		
		return normweights


	# update Probability of arm. Input is the current normalized weight dictionary and the index. Returns normilized probabilities.
	def updateProbability(self, index, normweight, probabilities):
		"""
		Update the probability for the index from its weight.
		"""
		
		print("\nWorking on probabilities...")
		for i in probabilities:
		#{'Sample A prob': 0.25, 'Sample B prob': 0.25, 'Sample C prob': 0.25, 'Sample D prob': 0.25}
			for j in normweight:
				if self.convention_converter(i) == self.convention_converter(j):
					#print(i, j)
					probabilities[i] = (normweight[j] * (1 - self.expRate)) + self.expRate * self.distParam
				#probabilities[prob_value] = (normweight[weight_value] * (1 - self.expRate)) + self.expRate * self.distParam
		
		self.probabilities = probabilities
		print ("Updated probabilities are:"+str(self.probabilities))
		print("Normalizing probabilities...")
		allprobabilities_sum = sum(probabilities.values())
		for p,value in probabilities.items():
			probabilities[p] = value/allprobabilities_sum
		self.probabilities = probabilities
		print("Normalized probabilities updated.")
		print("Normalized probabilities: "+str(self.probabilities))		
		
		return probabilities


	# Updates rewards for arms
	def reward_memory(self, reward, index, cumulative_reward):
		
		print("\nWorking on Rewards...")
		for r in cumulative_reward:
			if self.convention_converter(r) == index:
				print("Found matching index!")
				cumulative_reward[r] += int(reward)
				print(str(r) + "value updated to "+str(cumulative_reward[r]))
	
		self.cumulative_reward = cumulative_reward
		print("Updated cummulative rewards: "+str(self.cumulative_reward))
	
		return cumulative_reward


	def convention_converter(self,a_string):

		if a_string.startswith('Sample A'):
			index = 'Sample A'

		elif a_string.startswith('Sample B'):
			index = 'Sample B'

		elif a_string.startswith('Sample C'):
			index = 'Sample C'

		elif a_string.startswith('Sample D'):
			index = 'Sample D'

		else:
			print("\nnot found\n")
			index = 'Sample A'
		
		return index


banban = Bandit()
banban.main()