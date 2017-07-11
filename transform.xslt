<?xml version="1.0" encoding="UTF-8"?>
<mapping xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <model model="accounts.Country">
        <xsl:for-each select="//country">
            <item>
		<xsl:attribute name="key">
                    <xsl:value-of select="country_id"/>
                </xsl:attribute>
                <field name="name">
                    <xsl:value-of select="name"/>
                </field>
                <field name="code">
                    <xsl:value-of select="iso_code"/>
                </field>
            </item>
        </xsl:for-each>
    </model>

    <model model="accounts.State">
        <xsl:for-each select="//state_province">
            <item key="">
                <field name="name">
                    <xsl:value-of select="name"/>
                </field>
                <field name="code">
                    <xsl:value-of select="abbreviation"/>
                </field>
		<fk model="accounts.Country">
                    <xsl:attribute name="key">
                        <xsl:value-of select="country_id"/>
                    </xsl:attribute>
                </fk>
            </item>
        </xsl:for-each>
    </model>
</mapping>