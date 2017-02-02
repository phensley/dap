

// Append a pattern to the list of regexp for URLs to ignore.
//
// This assumes you've added a decide rule like the following to
// your crawler config:
//
// <bean class="org.archive.modules.deciderules.MatchesListRegexDecideRule">
//		  <property name="decision" value="REJECT"/>
//	 <property name="regexList">
//	 <list></list>
//	 </property>
// </bean>


import java.util.regex.*

regexObj = appCtx.getBean("scope").rules.find{
    it.class == org.archive.modules.deciderules.MatchesListRegexDecideRule 
}

// Set the regexp pattern for URLs to block from adding to the frontier
pattern = Pattern.compile("^https?://ofmpub.epa.gov/waters10/.*")
regexObj.regexList.add(pattern)

rawOut.println(regexObj.regexList)

